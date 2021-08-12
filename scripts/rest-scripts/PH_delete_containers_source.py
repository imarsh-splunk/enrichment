import argparse
import os
import sys

sys.path.append('/opt/phantom/lib')
sys.path.append('/opt/phantom/www')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'phantom_ui.settings')

import django

django.setup()
from django.db.utils import ProgrammingError

from phantom_ui.ui.models import *

VERSION = '4.0.0'


def running_playbooks_for_ids(cursor, container_ids):
    cid_sql = ','.join(['%s'] * len(container_ids))
    running_containers_sql = """
SELECT container_id from playbook_run WHERE container_id IN ({}) AND status = 'running'
""".format(cid_sql)


def main():
    argp = argparse.ArgumentParser(
            description='Tool to delete containers and related records '
                        'permanently from the system. Version {}'.format
            (VERSION)
    )
    argp.add_argument(
            '-b',
            '--list-labels',
            action='store_true',
            help="Lists available container labels and exits"
    )
    argp.add_argument(
            '-i',
            '--ids',
            default='',
            help="Comma separated list of IDs of the container to delete"
    )
    argp.add_argument(
            '-l',
            '--label',
            help="Only delete containers with this label"
    )
    argp.add_argument(
            '-m',
            '--matching',
            help="Title matches this string (case insensitive)"
    )
    argp.add_argument(
            '-v',
            '--verbose',
            action='store_true',
            help="Print names and IDs of containers to be deleted"
    )
    argp.add_argument(
            '-d',
            '--dry-run',
            action='store_true',
            help="Do not actually delete, just show output"
    )

    args = argp.parse_args()
    filters = {}

    if args.list_labels:
        try:
            with transaction.atomic():
                containers = Container.objects.distinct('label')
            print('Labels:')
            for container in containers:
                print('"{}"'.format(container.label))
            print('Done listing')
        except:
            traceback.print_exc()
            sys.exit(-1)
        sys.exit(0)

    if args.ids:
        try:
            filters['id__in'] = [
                int(x.strip()) for x in args.ids.split(',') if x.strip()
            ]
        except:
            print "Invalid value for container ID"
            sys.exit(-1)
    if args.label:
        filters['label'] = args.label

    if args.matching:
        filters['name__icontains'] = args.matching

    if not args.ids and not args.matching and not args.label:
        print 'ERROR: supply at least one argument'
        argp.print_help()
        sys.exit(-1)

    container_count = Container.objects.filter(**filters).count()
    if not container_count:
        print 'No containers matched the arguments. Nothing to do...'
        sys.exit(0)

    # We build a related_filters dictionary to access & filter related
    # models directly
    related_filters = dict()
    for k, v in filters.items():
        related_filters['container__' + k] = v

    actionrun_count = ActionRun.objects.filter(**related_filters).count()
    playbookrun_count = PlaybookRun.objects.filter(
        **related_filters).count()
    artifact_count = Artifact.objects.filter(**related_filters).count()
    report_count = Report.objects.filter(**related_filters).count()

    print 'Will delete {} containers with {} associated artifacts, {} ' \
          'playbook executions {} reports and {} action_executions.'. \
        format(container_count, artifact_count, playbookrun_count, \
               report_count, actionrun_count)

    if args.dry_run:
        sys.exit(0)

    # Ask for confirmation on this destructive action
    print 'This will permanently delete data from the system. Consider ' \
          'taking a backup before proceeding.'

    answer = raw_input('Do you wish to continue [y/N]: ')
    if answer.lower() not in ('y', 'yes'):
        print 'Cancelling...'
        sys.exit(0)

    params = list()
    sql = """SELECT id AS id FROM container WHERE"""

    if args.label:
        # If user has provided a label on command line
        sql += " label = %s"
        params.append(args.label)

    if args.matching:
        # if user has provided name pattern
        if len(params):
            sql += " AND UPPER(name) LIKE UPPER(%s)"
        else:
            sql += " UPPER(name) LIKE UPPER(%s)"
        params.append('%' + args.matching + '%')

    if args.ids:
        # if user has provided comma separated ids
        id_list = [int(x.strip()) for x in args.ids.split(',') if
                   x.strip()]
        id_sql = ','.join(['%s'] * len(id_list))
        if len(params):
            sql += " AND id IN ({})".format(id_sql)
        else:
            sql += " id IN ({})".format(id_sql)
        params.extend(id_list)

    # fetch 50K rows at a time
    sql += " LIMIT 50000"
    cursor = Container.get_cursor()

    while True:
        try:
            cursor.execute(sql, params)
            rows = cursor.fetchall()
        except ProgrammingError:
            # no more rows
            break

        if not len(rows):
            # Sanity check if no rows
            break

        container_ids = [row[0] for row in rows]
        cid_sql = ','.join(['%s'] * len(container_ids))

        common_sql = "DELETE FROM {} WHERE container_id IN (" + cid_sql + \
                     ")"

        """
        To delete tables, we need to follow the order of FK dependencies.
        So, for example - to delete container, we need to delete action_run
        first. To delete action run, we need to delete app_run and 
        caes_action_run
        first
        """
        with transaction.atomic():

            """
            Begin delete of approvals
            """
            print running_playbooks_for_ids(cursor, container_ids)

            # Update approvals who have a action_run FK to one of the
            # containers we want to delete
            update_sql = """
                            UPDATE approval SET 
                            escalated_approval_id = NULL, parent_id 
                            = NULL WHERE action_run_id IN (SELECT id 
                            FROM action_run WHERE container_id IN ({}))
                        """.format(cid_sql)
            cursor.execute(update_sql, container_ids)

            # Actual delete of the approvals
            approval_sql = """
                            DELETE FROM approval WHERE action_run_id 
                            IN (SELECT id 
                            from action_run WHERE container_id IN ({}))
                        """.format(cid_sql)
            cursor.execute(approval_sql, container_ids)

            # Delete app runs before deleting action runs
            cursor.execute(common_sql.format('app_run'), container_ids)

            # update case action run maps to set src action run ids to null
            caseactionrun_sql = """
                UPDATE case_action_run_map SET source_action_run_id = NULL 
                  WHERE source_action_run_id in 
                    (
                    SELECT id FROM action_run WHERE container_id in ({})
                    )
            """.format(cid_sql)
            cursor.execute(caseactionrun_sql, container_ids)

            caseactionrun_sql = """
                DELETE FROM case_action_run_map WHERE case_action_run_id
                IN 
                (
                  SELECT id from action_run WHERE container_id in ({})
                )
            """.format(cid_sql)
            cursor.execute(caseactionrun_sql, container_ids)

            # delete the action runs
            cursor.execute(common_sql.format('action_run'), container_ids)

            # Delete playbook_run and its dependencies
            cursor.execute(common_sql.format(
                    'playbook_history'),
                    container_ids
            )
            approval_pb_sql = """
                DELETE FROM approval 
                  WHERE playbook_run_id IN 
                  (
                    SELECT id from playbook_run WHERE container_id IN ({})
                    )
            """.format(cid_sql)
            cursor.execute(approval_pb_sql, container_ids)

            playbookrunlog_sql = """
                DELETE FROM playbook_run_log 
                WHERE playbook_run_id IN 
                (
                SELECT id FROM playbook_run WHERE container_id IN ({})
                )
            """.format(cid_sql)
            cursor.execute(playbookrunlog_sql, container_ids)

            casepbrun_sql = """
                UPDATE case_playbook_run_map  SET source_playbook_run_id 
                = NULL
                WHERE source_playbook_run_id IN 
                (
                SELECT id FROM playbook_run WHERE container_id in ({})
                )
            """.format(cid_sql)
            cursor.execute(casepbrun_sql, container_ids)

            casepbrun_sql = """
                DELETE FROM case_playbook_run_map WHERE 
                case_playbook_run_id
                IN 
                  (
                    SELECT id FROM playbook_run WHERE container_id in ({})
                  )
            """.format(cid_sql)
            cursor.execute(casepbrun_sql, container_ids)

            # Delete artifact and its dependencies
            caseartifact_sql = """
                                UPDATE case_artifact_map SET 
                                source_artifact_id = NULL 
                                WHERE source_artifact_id IN 
                                (
                                SELECT id from artifact WHERE 
                                container_id in ({})
                                )
                            """.format(cid_sql)
            cursor.execute(caseartifact_sql, container_ids)

            caseartifact_sql = """
                                DELETE FROM case_artifact_map 
                                WHERE case_artifact_id 
                                IN 
                                (
                                SELECT id from artifact 
                                WHERE 
                                container_id in ({})
                                )
                            """.format(cid_sql)
            cursor.execute(caseartifact_sql, container_ids)

            indicator_artifact_record_sql = """
                DELETE FROM indicator_artifact_record
                WHERE artifact_id IN (
                  SELECT id FROM artifact WHERE container_id in ({})
                )
            """.format(cid_sql)
            cursor.execute(indicator_artifact_record_sql, container_ids)

            cursor.execute(common_sql.format('artifact'), container_ids)

            # Delete actual playbook runs
            cursor.execute(common_sql.format('playbook_run'),
                           container_ids)

            # Delete report and its dependencies
            reportrun_sql = """
                DELETE FROM report_run 
                WHERE template_id IN 
                ( 
                SELECT id from report WHERE container_id IN ({})
                )
            """.format(cid_sql)
            cursor.execute(reportrun_sql, container_ids)
            cursor.execute(common_sql.format('report'), container_ids)

            # Delete container attachment and its dependencies
            caseconattachment_sql = """
                UPDATE case_vault_map SET source_attachment_id = NULL 
                WHERE source_attachment_id IN 
                (
                SELECT id from container_attachment WHERE container_id 
                in ({})
                )
            """.format(cid_sql)
            cursor.execute(caseconattachment_sql, container_ids)

            caseconattachment_sql = """
                DELETE FROM case_vault_map WHERE case_attachment_id IN 
                (
                  SELECT id FROM container_attachment WHERE container_id 
                  in ({})
                )
            """.format(cid_sql)
            cursor.execute(caseconattachment_sql, container_ids)

            cursor.execute(common_sql.format('container_attachment'),
                           container_ids)

            # Delete container and its dependencies
            casecontainer_sql = """
                UPDATE case_container_map SET source_container_id = NULL 
                WHERE source_container_id IN ({})

            """.format(cid_sql)
            cursor.execute(casecontainer_sql, container_ids)

            casecontainer_sql = """
                                DELETE FROM case_container_map
                                WHERE case_container_id IN ({})
                            """.format(cid_sql)
            cursor.execute(casecontainer_sql, container_ids)

            cursor.execute(common_sql.format('chunked_upload'),
                           container_ids)
            cursor.execute(common_sql.format('container_comment'),
                           container_ids)
            cursor.execute(common_sql.format('container_note'),
                           container_ids)
            cursor.execute(common_sql.format('container_pin'),
                           container_ids)
            cursor.execute(common_sql.format('container_audit_trail'),
                           container_ids)
            cursor.execute(common_sql.format('automation_data'),
                           container_ids)
            cursor.execute(common_sql.format('workflow_note'),
                           container_ids)
            cursor.execute(common_sql.format('workflow_task'),
                           container_ids)

            containernote_sql = """
                DELETE FROM container_note WHERE phase_id IN 
                  ( 
                    SELECT id from workflow_phase WHERE container_id IN 
                    ({})
                  )
            """.format(cid_sql)
            cursor.execute(containernote_sql, container_ids)

            cursor.execute(common_sql.format('workflow_phase'),
                           container_ids)
            caseactivity_sql = """
                DELETE FROM case_activity WHERE case_id IN ({})
            """.format(cid_sql)
            cursor.execute(caseactivity_sql, container_ids)

            container_sql = """
                DELETE FROM container WHERE id IN ({})
            """.format(cid_sql)
            cursor.execute(container_sql, container_ids)

            # Delete vault documents which have no container attachments
            vault_items = VaultDocument.objects.annotate(
                    ct=Count('containerattachment')).filter(ct=0)

            for doc in vault_items.iterator():
                if os.path.abspath(doc.path).startswith(
                        '/opt/phantom/vault/'
                ) and os.path.isfile(doc.path):
                    os.unlink(doc.path)
                doc.delete()

    print 'Successfully deleted containers.\n'


if __name__ == '__main__':
    main()