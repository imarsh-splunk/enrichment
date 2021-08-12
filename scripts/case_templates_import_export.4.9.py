import argparse
import getpass
import json
import io
import os
import sys
import tarfile
import traceback
import shutil
from collections import OrderedDict

if sys.version_info[0] == 2:
    print("This script does not work in python2, please run with python3")
    sys.exit(1)

from django.utils import timezone

sys.path.append('/opt/phantom/lib')
sys.path.append('/opt/phantom/www')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'phantom_ui.settings')
import django

django.setup()
from django.db import transaction
from phantom_ui.ui.models.case_workflow import (
    WorkflowTemplate, WorkflowPhaseTemplate, WorkflowTaskTemplate
)
from phantom_ui.ui.models.playbook import Playbook, SCM
from phantom_ui.ui.models.user import PhUser
from phantom_ui.phplaybooks import git_helper
from phantom_ui.ui.shared import serialize_model
from phantom_ui.ui.ipc import create_ipc, kValidatePlaybook, kLoadPlaybook, send_ipc, urlopen

VERSION = '4.0.0'


def clean_playbook_import(dest_dir):
    try:
        if os.path.isdir(dest_dir):
            shutil.rmtree(dest_dir)
    except:
        pass


def is_playbook_path_valid(scm, playbook):
    """
    Helper function to make sure the user is not trying directory traversal in
    playbook json
    Args:
        scm (str): name of the git repo
        playbook (str): name of the playbook

    Returns:
        bool
    """
    playbook_path = os.path.join('/opt', 'phantom', 'scm', 'git', scm, playbook)
    if not os.path.realpath(playbook_path).startswith('/opt/phantom/scm/git/{}'.format(scm)):
        return False
    return True


def notify_playbook_update():
    notify_data = [{'playbook': 'playbook'}]
    _ = urlopen('http://127.0.0.1:8888/notify', json.dumps(notify_data).encode("UTF-8"))


def process_playbook(item, repo, dest_dir, user, template_name):
    """
    Helper function which creates playbook instance from the incoming
    case template import
    Args:
        item (dict): dictionary which has 'scm' and 'playbook' keys
        repo (str): The repo in which to impport the
        dest_dir (str): path to where the archive was extracted
        template_name (str): The template name to be used in the playbook comm
                                ent
    Returns:

    """
    scm = SCM.objects.filter(name=repo, disabled=False).first()
    playbook = Playbook.create_playbook(scm.id)
    playbooks_dir = os.path.join(dest_dir, 'playbooks', item['playbook'])

    if not os.path.realpath(playbooks_dir).startswith(dest_dir):
        raise Exception('Invalid value in playbook json: ' + item['playbook'])

    py_data = open(playbooks_dir + '.py').read()
    json_data = json.loads(open(playbooks_dir + '.json').read().encode('utf-8'))

    playbook.python = py_data.decode('utf-8')
    playbook.blockly = json_data.get('blockly', False)
    playbook.blockly_xml = json_data.get('blockly_xml')
    playbook.category = json_data.get('category', 'Uncategorized')
    playbook.comment = 'Imported from case template {}'.format(template_name)
    playbook.labels = json_data.get('labels', [])
    playbook.name = item['playbook']
    playbook.draft_mode = True
    playbook.passed_validation = not playbook.draft_mode
    if not is_playbook_path_valid(repo, item['playbook']):
        raise Exception(
            'Invalid values in playbook json for either ' + repo + ' or ' + item['playbook']
        )

    playbook.playbook_file_path = os.path.join(
        '/opt', 'phantom', 'scm', 'git', repo, item['playbook']
    )
    playbook.coa_data = json_data.get('coa', {}).get('data', {})
    playbook.platform_version = json_data.get('coa', {}).get('version', '1.0')
    playbook.coa_schema_version = json_data.get('coa', {}).get('schema', 1)
    playbook.log_level = 0
    playbook.safe_mode = False
    playbook.active = False
    playbook.set_tags(item.get('tags', []))
    playbook.latest_editor = user
    playbook.save()

    ipc = create_ipc(kValidatePlaybook, [playbook.id])
    ipc_response = send_ipc(ipc)
    if ipc_response['result']['status'] == 'success':
        playbook.draft_mode = False
        playbook.save(update_custom_function_association=False)
        try:
            ipc = create_ipc(kLoadPlaybook, [playbook.id])
            _ = send_ipc(ipc)
        except Exception:
            pass
    git_helper.save_new_revision(playbook, user)
    notify_playbook_update()


def export_case_template(qs, verbose=False):
    """
    Exports case template(s) to a tarball, which is written in the same
    directory from where this command is run
    Args:
        ids (list): list of case template ids to be exported
        verbose (bool): flag to indicate where to show verbose output
    Returns:
    """
    result = list()
    playbooks = list()

    try:
        print('Starting export of case templates')
        for template in qs.order_by('id').iterator():
            if verbose:
                print('Exporting case template: {}'.format(template.name))

            serialized_tmpl_data = serialize_model(WorkflowTemplate, template)
            json_obj = OrderedDict({
                'name': serialized_tmpl_data['name'],
                'status': serialized_tmpl_data['status'],
                'is_default': serialized_tmpl_data['is_default']
            })

            phases = list()
            # Iterate over the phases in this template
            for phase in template.phases.order_by('order'):
                if verbose:
                    print('Exporting template phase: {} for case template' \
                          ': {}'.format(phase.name, template.name))
                serialized_phase_data = serialize_model(WorkflowPhaseTemplate, phase)
                phase_obj = OrderedDict({
                    'name': serialized_phase_data['name'],
                    'order': serialized_phase_data['order']
                })
                tasks = list()

                # Iterate over the tasks in this phase
                for task in serialized_phase_data['tasks']:
                    if verbose:
                        print('Exporting task: {} for phase: {} of case template: {}'.\
                            format(task['name'], phase.name, template.name))
                    task_obj = OrderedDict({
                        'name': task['name'],
                        'description': task['description'],
                        'order': task['order'],
                        'suggestions': task['suggestions']
                    })
                    """
                    If there are any suggested playbooks, add them to the
                    playbooks list - we will create a tarball with them later
                    """
                    if 'playbooks' in task['suggestions']:
                        playbooks.extend(task['suggestions']['playbooks'])

                    tasks.append(task_obj)

                # All tasks for this phase are processed, add it to our dict
                phase_obj['tasks'] = tasks

                # Finished processing this phase, add it to our phases list
                phases.append(phase_obj)

            # All phases for this template are processed, add it to our dict
            json_obj['phases'] = phases
            result.append(json_obj)

            if verbose:
                print('Finished exporting case template: {}'.format(template.name))

        # Lets create a tarball of the output json
        tarname = 'case_template_impexp_{}'.format(timezone.now().strftime('%m-%d-%Y-%M%S'))

        if verbose:
            print('Adding case template info to tarfile')

        tarf = tarfile.open(tarname + '.tgz', mode='w:gz')
        json_info = tarfile.TarInfo(name='template.json')
        json_dump = json.dumps(result, indent=4)
        json_info.size = len(json_dump)
        tarf.addfile(tarinfo=json_info, fileobj=io.BytesIO(json_dump.encode('utf-8')))

        # Add the playbooks to the tarball
        for item in playbooks:
            if verbose:
                print('Adding related playbook: {} to tarfile'.format(item['playbook']))

            # Sanity check to make sure path not malicious
            if not is_playbook_path_valid(item['scm'], item['playbook']):
                print('Invalid values in playbook json for either scm: {} ' \
                      'or playbook name: {} '.format(item['scm'], item['playbook']))
                continue

            path = os.path.join('/opt', 'phantom', 'scm', 'git', item['scm'], item['playbook'])

            # Make sure the playbook py and json files exist
            py_path = path + '.py'
            json_path = path + '.json'
            if not os.path.isfile(py_path) or not os.path.isfile(json_path):
                if verbose:
                    print('Could not find the files for playbook {} in the ' \
                          'repo {}'.format(item['playbook'], item['scm']))
                continue

            tarf.add(py_path, arcname='playbooks/{}.py'.format(item['playbook']))
            tarf.add(json_path, arcname='playbooks/{}.json'.format(item['playbook']))

        tarf.close()
        print('Finished exporting case templates to archive: {}'.format(tarname))
    except:
        traceback.print_exc()
        sys.exit(-1)


def validate_tarball(file_path, dest_dir):
    """

    Args:
        file_path (str): The path to the tarball provided by the user
        dest_dir (str): The path to the tmp directory under /opt/phantom where
                        the tarball will be extracted
    Returns:

    """
    f = tarfile.open(file_path, 'r|*')
    full_path = None
    for tarinfo in f:
        if tarinfo.issym():
            raise Exception(
                'Found symbolic link in tarball %r. Symbolic links '
                'are not allowed.' % file_path
            )
        path = tarinfo.name
        if full_path is None:
            full_path = path
        path = os.path.realpath(os.path.join(dest_dir, path))
        if not path.startswith(dest_dir):
            raise Exception('Invalid path found in tarball %r.' % full_path)
    if full_path is None:
        raise Exception('No files not found in package.')

    # extract the rest of the members
    f.close()


def import_case_template(file_path, user=None, scm=None, verbose=False):
    """
    Imports a tarball having case template data
    Args:
        file_path (str): Path to the archive from which case template data will
                            be imported
        user (PhUser): User object which will be associated with the related
                        playbooks (if any) for a task
        scm (str): Repo name where playbooks should be imported into
        verbose (bool): Higher verbosity
    """
    dest_dir = '/opt/phantom/tmp/casetemplate_import_export_{}'.format(
        timezone.now().strftime('%m-%d-%Y-%M%S')
    )
    try:
        print('Starting import of case templates')
        os.mkdir(dest_dir)

        # Validate incoming tarball to make sure no directory traversal
        validate_tarball(file_path, dest_dir)
        tarf = tarfile.open(file_path, 'r:gz')
        tarf.extractall(path=dest_dir)
        os.chdir(dest_dir)
        json_file_path = os.path.join(dest_dir, 'template.json')
        if not os.path.isfile(json_file_path):
            print('Invalid archive. Could not find the template.json in the' \
                  'archive')
            sys.exit(-1)
        try:
            template_data = json.loads(open(json_file_path).read())
        except ValueError:
            print('Aborting import. Could not parse the template.json in the '\
                  'archive.')
            sys.exit(-1)

        with transaction.atomic():
            for template in template_data:
                if verbose:
                    print('Processing case template: {}'.format(template['name']))

                tmpl_resp = WorkflowTemplate.rest_create({
                    'name': template['name'],
                    'is_default': template['is_default']
                }, user, None)
                # Iterate over the template phases
                for phase in template['phases']:
                    if verbose:
                        print(
                            'Processing Phase {} for template {}'.format(
                                phase['name'], template['name']
                            )
                        )

                    phase_resp = WorkflowPhaseTemplate.rest_create({
                        'template_id': json.loads(tmpl_resp.content)['id'],
                        'name': phase['name'],
                        'order': phase['order']
                    }, user, None)

                    # Iterate over the tasks
                    for task in phase['tasks']:
                        if verbose:
                            print(
                                'Processing task: {} for phase: {} of template: {}'.format(
                                    task['name'], phase['name'], template['name']
                                )
                            )

                        sanitized_suggestions = dict()

                        if 'actions' in task['suggestions']:
                            sanitized_suggestions['actions'] = task['suggestions']['actions']
                        else:
                            sanitized_suggestions['actions'] = list()
                        # look into the playbooks suggestions for a task
                        if 'playbooks' in task['suggestions']:
                            sanitized_suggestions['playbooks'] = list()

                            for item in task['suggestions']['playbooks']:
                                repo = scm or item['scm']
                                target_dir = os.path.join('/opt', 'phantom', 'scm', 'git', repo)
                                # Does the git repo exist on target ova ?
                                # If not, dont process this playbook
                                if not os.path.isdir(os.path.realpath(target_dir)):
                                    print(
                                        'Could not find repo {} on system. Aborting import of playbook {}'
                                        .format(repo, item['playbook'])
                                    )

                                elif not is_playbook_path_valid(repo, item['playbook']):
                                    print(
                                        'Invalid path found when attempting to import playbook {} into repo {}'
                                        .format(item['playbook'], repo)
                                    )

                                # If the playbook already exists on target
                                # system, dont process
                                elif os.path.isfile(
                                    os.path.join(target_dir, '{}.py'.format(item['playbook']))
                                ):
                                    if scm:
                                        # If user provided scm value when importing, the scm for the playbook suggestion needs to be set to it
                                        item['scm'] = scm
                                    sanitized_suggestions['playbooks'].append(item)
                                else:
                                    # We will process this playbook
                                    try:
                                        process_playbook(
                                            item, repo, dest_dir, user, template['name']
                                        )
                                        if scm:
                                            item['scm'] = scm
                                        sanitized_suggestions['playbooks'].append(item)
                                    except Exception as e:
                                        # FIXME: Python3-incompatible exception-handling
                                        if verbose:
                                            traceback.print_exc()
                                        print(
                                            'Unexpected problem {} while importing playbook {}...Continuing to next playbook'
                                            .format(e.message, item['playbook'])
                                        )
                        else:
                            sanitized_suggestions['playbooks'] = list()
                        _ = WorkflowTaskTemplate.rest_create({
                            'phase_id': json.loads(phase_resp.content)['id'],
                            'name': task['name'],
                            'order': task['order'],
                            'description': task['description'],
                            'actions': sanitized_suggestions['actions'],
                            'playbooks': sanitized_suggestions['playbooks']
                        }, user, None)

        print('Finished importing case templates')
    except Exception as e:
        # FIXME: Python3-incompatible exception-handling
        if verbose:
            traceback.print_exc()
        else:
            print('Unexpected problem {} when importing case templates'.format(e.message))

    finally:
        clean_playbook_import(dest_dir)


def call_import_export_case_templates():
    argp = argparse.ArgumentParser(
        description='Script to import and export case templates from the '
        'system. Version {}'.format(VERSION)
    )
    argp.add_argument(
        '-e',
        '--export',
        dest='export_template',
        action='store_true',
        help='Provide this flag if exporting case templates'
    )
    argp.add_argument(
        '-i',
        '--import',
        dest='import_template',
        action='store_true',
        help='Provide this flag if importing case templates'
    )
    argp.add_argument(
        '-k',
        '--ids',
        type=str,
        help='Comma separated list of IDs of the case templates you want '
        'to export. If no IDs are provided, all case templates will  '
        'be exported'
    )
    argp.add_argument(
        '-f',
        '--file',
        type=str,
        help='The absolute path to the archive which has the case templates to be '
        'imported into the system'
    )
    argp.add_argument(
        '-n',
        '--names',
        nargs='+',
        help='Comma separated list of case template names (in quotes) to be'
        ' exported'
    )
    argp.add_argument(
        '-s',
        '--scm',
        dest='dest_repo',
        type=str,
        help='The repo into which the playbooks associated with tasks will'
        'be imported into. This is an optional argument. If not '
        ' provided, the playbooks will be attempted to be imported '
        'into a repo with the same name from which they were exported'
    )
    argp.add_argument('-v', '--verbose', action='store_true', help='Increased verbosity')

    # Check for validity of args
    args = argp.parse_args()
    if not args.export_template and not args.import_template:
        print('At lease one of export or import flag is needed')
        sys.exit(-1)

    if args.export_template and args.import_template:
        print('Only one of export or import should be ' \
              'provided at one time')
        sys.exit(-1)

    if args.import_template and not args.file:
        print('When importing case template, please provide location of ' \
              'tarball file from which the templates will be imported')
        sys.exit(-1)
    if args.export_template and args.ids and args.names:
        print('When importing case template, provide either a list of comma ' \
              'separated case template ids or a list of comma separated case ' \
              'template names')

    if args.import_template and args.dest_repo:
        # User has provided destination repo - validate it exists
        target_dir = os.path.join('/opt', 'phantom', 'scm', 'git', args.dest_repo)
        if not os.path.isdir(target_dir) or not os.path.realpath(target_dir).\
                startswith('/opt/phantom/scm/git/{}'.format(args.dest_repo)):
            print('Invalid value provided for scm argument. ')
            sys.exit(-1)

    cleaned_ids = list()
    # Case templates filtered by id
    if args.export_template and args.ids:
        cleaned_ids = [int(x.strip()) for x in args.ids.split(',') if x.strip()]
        qs = WorkflowTemplate.objects.filter(id__in=cleaned_ids)
        if not qs.count():
            print('Could not find any case templates with the specified id(s)')
            sys.exit(-1)

    # Case templates filtered by names
    elif args.export_template and args.names:
        qs = WorkflowTemplate.objects.filter(name__in=args.names)
        if not qs.count():
            print('Could not find any case templates with matching names')
            sys.exit(-1)

    # Get all case templates
    elif args.export_template and not args.ids and not args.names:
        qs = WorkflowTemplate.objects.all()

    while True:
        username = input('Enter username: ')
        password = getpass.getpass()
        try:
            user = PhUser.objects.get(username=username, is_active=True)
            if not user.check_password(password):
                print('Please provide a valid username and password')
            else:
                break
        except PhUser.DoesNotExist:
            print('Please provide a valid username and password')

    if args.export_template:
        export_case_template(qs, verbose=args.verbose)

    elif args.import_template:
        import_case_template(args.file, user=user, scm=args.dest_repo, verbose=args.verbose)


if __name__ == '__main__':
    call_import_export_case_templates()
