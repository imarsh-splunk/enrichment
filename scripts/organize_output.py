#!/usr/bin/env python2.7

import json
import argparse
from collections import OrderedDict

STATUS_PATH = 'action_result.status'
PARAM_PATH = 'action_result.parameter'
DATA_PATH = 'action_result.data'
ACTION_SUMMARY_PATH = 'action_result.summary'
MESSAGE_PATH = 'action_result.message'
SUMMARY_PATH = 'summary.'


def cleanup_action_output(action):
    if action['action'] == "on poll":
        print "Ignoring on poll"
        return
    elif action['action'] == "test connectivity":
        print "Ignoring test connectivity"
        return

    print "Cleaning up %s" % action['action']

    parameter_map = {}
    parameter_list = []
    data_list = []
    action_summary_list = []
    status_list = []

    output_ordering = [
        (STATUS_PATH, status_list),
        (PARAM_PATH, parameter_list),  # we want to use this list later
        (DATA_PATH, data_list),
        (ACTION_SUMMARY_PATH, action_summary_list),
        (MESSAGE_PATH, []),
        (SUMMARY_PATH, [])
    ]

    # Get a list (map) of parameters
    for k, v in action['parameters'].iteritems():
        if v['data_type'] == 'ph':
            continue
        parameter_map['{}.{}'.format(PARAM_PATH, k)] = {
            'data_type': v['data_type'],
            'contains': v.get('contains')

        }

    for data_path in action['output']:
        for pair in output_ordering:
            if data_path['data_path'].startswith(pair[0]):
                if pair[0] == PARAM_PATH:
                    # Remove any found paremters from list
                    parameter_map.pop(data_path['data_path'], None)
                pair[1].append(data_path)
                break

    # Add default value if following lists are empty
    if not data_list:
        print "Adding default path for action_result.data"
        data_list.append({
            'data_path': 'action_result.data',
            'data_type': 'string'
        })
    if not action_summary_list:
        print "Adding default path for action_result.summary"
        action_summary_list.append({
            'data_path': 'action_result.summary',
            'data_type': 'string'
        })
    if not status_list:
        print "Adding default path for action_result.status"
        status_list.append({
            'data_path': 'action_result.status',
            'data_type': 'string',
            'example_values': [
                'success',
            ]
        })

    # Add remaining parameters to output
    for k, v in parameter_map.iteritems():
        print "Adding parameter data path: {}".format(k)
        new_data_path = OrderedDict({
            'data_path': k,
            'data_type': v['data_type']
        })
        if v['contains'] is not None:
            new_data_path['contains'] = v['contains']
        parameter_list.append(new_data_path)

    new_output_list = []
    for pair in output_ordering:
        new_output_list.extend(sorted(pair[1], key=lambda x: x['data_path']))

    action['output'] = new_output_list
    return


def main(app_json_path):
    try:
        fp = open(app_json_path, 'r+')
    except Exception as e:
        print "Error opening file"
        print str(e)
        exit(1)

    try:
        app_json = json.loads(fp.read(), object_pairs_hook=OrderedDict)
    except Exception as e:
        print "Error reading app JSON"
        print str(e)
        exit(1)

    for action in app_json['actions']:
        cleanup_action_output(action)

    print "Updating file..."
    fp.seek(0)
    json.dump(app_json, fp, sort_keys=False, indent=4, separators=(',', ': '))
    fp.truncate()
    fp.flush()
    fp.close()
    print "Done"
    return


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description="Order the output")
    argparser.add_argument('app_json_path', help="App JSON")
    args = argparser.parse_args()

    d = vars(args)
    main(**d)