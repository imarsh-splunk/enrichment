#!/usr/local/bin/python3

import argparse
import datetime
import os
import requests
import yaml
import uuid
import keyring

# setup logging to stdout and file
import logging

log_formatter = logging.Formatter("%(asctime)s [%(levelname)-4.4s]  %(message)s")
logger = logging.getLogger("my_logger")
logger.setLevel(logging.DEBUG)

log_path = os.path.realpath(__file__) + ".log"
print("logging to {}".format(log_path))
file_handler = logging.FileHandler(log_path)
file_handler.setFormatter(log_formatter)
logger.addHandler(file_handler)

terminal_handler = logging.StreamHandler()
terminal_handler.setFormatter(log_formatter)
logger.addHandler(terminal_handler)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--workbook_id', help="the id of the workbook to pull")
    args = parser.parse_args()

    logger.debug("starting at {} with args {}".format(datetime.datetime.now(), args))

    phantom_base = keyring.get_password("internal oar content", "phantom base url")
    phantom_auth_token = keyring.get_password("internal oar content", "phantom auth token")
    headers = {
        "ph-auth-token": phantom_auth_token
    }
    
    # fetch the top-level workbook, which is basically just the name and description with no content
    workbook = requests.get(phantom_base + 'rest/workbook_template/{}'.format(args.workbook_id), headers=headers, verify=False).json()
    workbook['id'] = str(uuid.uuid4())
    workbook['how_to_implement'] = ''
    del workbook['creator']
    del workbook['is_default']
    del workbook['is_note_required']
    del workbook['status']
    workbook['phases'] = []
    logger.debug(workbook)

    # fetch all the phases of the template
    params = {"page_size": 0, "_filter_template": args.workbook_id}
    phases_url = phantom_base + "/rest/workbook_phase_template"
    r = requests.get(phases_url, params=params, headers=headers, verify=False)
    phases = r.json()['data']
    phases.sort(key=lambda p: p['order'])
    logger.debug(phases)

    # fetch all the tasks for each phase
    tasks = []
    for phase in phases:
        # the phase will have a uuid in the repo, which will replace the local id in phantom
        phase_uuid = str(uuid.uuid4())
        phantom_phase_id = phase['id']
        phase['id'] = phase_uuid
        phase['how_to_implement'] = ""
        del phase['template']
        del phase['sla']
        del phase['sla_type']
        del phase['order']
        phase_in_workbook = {
            'id': phase_uuid,
            'name': phase['name']
        }
        workbook['phases'].append(phase_in_workbook)
        phase['tasks'] = []
        params = {"page_size": 0, "_filter_phase": phantom_phase_id}
        task_url = phantom_base + "/rest/workbook_task_template"
        r = requests.get(task_url, params=params, headers=headers, verify=False)
        for task in r.json()['data']:
            task['id'] = str(uuid.uuid4())
            task['how_to_implement'] = ""
            task_in_phase = {
                'id': task['id'],
                'name': task['name']
            }
            phase['tasks'].append(task_in_phase)
            tasks.append(task)

    # write the tasks to their respective yamls
    for task in tasks:
        file_path = './workbook_downloads/workbooks/phases/tasks/{}.yml'.format(task['name']).replace(' ', '_')
        with open(file_path, 'w') as f:
            f.write(yaml.dump(task))

    # write the phases to their respective yamls
    for phase in phases:
        file_path = './workbook_downloads/workbooks/phases/{}.yml'.format(phase['name']).replace(' ', '_')
        with open(file_path, 'w') as f:
            f.write(yaml.dump(phase))

    # write the workbook to a yaml
    file_path = './workbook_downloads/workbooks/{}.yml'.format(workbook['name']).replace(' ', '_')
    with open(file_path, 'w') as f:
        f.write(yaml.dump(workbook))

if __name__ == '__main__':
    main()
