import os, sys, csv
import time
import json
import requests

AUTH_TOKEN = '*****************************'
server  = 'https://127.0.0.1/'

live_containers=[]
dead_containers={}
active_playbooks={}
repos={}

headers = {
  "ph-auth-token": AUTH_TOKEN
}

requests.packages.urllib3.disable_warnings()

###########################################################
### Get containers that already had playbooks run
###########################################################
query_url = '{0}rest/playbook_run?page_size=1000&sort=id&order=desc&_filter_start_time__gt="2019-06-09T00:00:00.000000Z"'.format( server )
response = json.loads( requests.get( query_url, headers=headers, verify=False ).text )

for entry in response['data']:
    if entry['status'] != 'success':
        print "{0}\t\t{1}\t\t{2}\t\t{3}".format( entry['id'], entry['container'], entry['status'], entry['start_time'] )
        #print entry['message']
    else:
        live_containers.append( entry['container'] )


###########################################################
### Find all containers that are left
###########################################################
query_url = '{0}rest/container?page_size=0&sort=id&order=desc&_filter_create_time__gt="2019-06-09T00:00:00.000000Z"'.format( server )
response = json.loads( requests.get( query_url, headers=headers, verify=False ).text )

for entry in response['data']:
    if entry['id'] not in live_containers:
        dead_containers[entry['id']] = entry['label']


###########################################################
### Build active playbook dictionary
###########################################################
query_url = '{0}rest/playbook?page_size=0&_filter_active="True"'.format( server )
response = json.loads( requests.get( query_url, headers=headers, verify=False ).text )

for entry in response['data']:
    for label in entry['labels']:
        label_matches = active_playbooks.get( label, [] )
        label_matches.append( entry['id'] )
        active_playbooks[label] = label_matches

print active_playbooks


###########################################################
### Execute playbooks against dead containers
###########################################################
query_url = '{0}rest/playbook_run'.format( server )
for container in dead_containers.keys():
    label = dead_containers[container]
    if active_playbooks.has_key( label ):
        for playbook in active_playbooks[label]:
            print 'Container: {0}\t\tLabel: {1}\t\tPlaybook: {2}'.format( container, label, playbook )
            response = requests.post(
                                    query_url,
                                    json={
                                        "container_id": container,
                                        "playbook_id": playbook,
                                        "scope": "all",
                                        "run": "true"
                                    },
                                    headers=headers,
                                    verify=False
                                )
            print response
            print response.text
            time.sleep( 4 )
