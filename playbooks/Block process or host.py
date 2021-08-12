"""
"""

import phantom.rules as phantom
import json
from datetime import datetime, timedelta
def on_start(container):
    phantom.debug('on_start() called')
    
    # call 'block_hash_3' block
    block_hash_3(container=container)

    return

def block_hash_3(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('block_hash_3() called')

    # collect data for 'block_hash_3' call
    container_data = phantom.collect2(container=container, datapath=['artifact:*.cef.fileHash', 'artifact:*.id'])

    parameters = []
    
    # build parameters list for 'block_hash_3' call
    for container_item in container_data:
        if container_item[0]:
            parameters.append({
                'hash': container_item[0],
                'comment': "",
                # context (artifact id) is added to associate results with the artifact
                'context': {'artifact_id': container_item[1]},
            })

    phantom.act(action="block hash", parameters=parameters, assets=['carbonblack'], callback=hunt_file_3, name="block_hash_3")

    return

def hunt_file_3(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('hunt_file_3() called')
        
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'hunt_file_3' call
    results_data_1 = phantom.collect2(container=container, datapath=['block_hash_3:action_result.parameter.hash', 'block_hash_3:action_result.parameter.context.artifact_id'], action_results=results)

    parameters = []
    
    # build parameters list for 'hunt_file_3' call
    for results_item_1 in results_data_1:
        if results_item_1[0]:
            parameters.append({
                'hash': results_item_1[0],
                'type': "",
                'range': "0-10",
                # context (artifact id) is added to associate results with the artifact
                'context': {'artifact_id': results_item_1[1]},
            })

    phantom.act(action="hunt file", parameters=parameters, assets=['carbonblack'], callback=quarantine_device_3, name="hunt_file_3", parent_action=action)

    return

def quarantine_device_3(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('quarantine_device_3() called')
        
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'quarantine_device_3' call
    results_data_1 = phantom.collect2(container=container, datapath=['hunt_file_3:action_result.data.*.process.results.*.hostname', 'hunt_file_3:action_result.parameter.context.artifact_id'], action_results=results)

    parameters = []
    
    # build parameters list for 'quarantine_device_3' call
    for results_item_1 in results_data_1:
        if results_item_1[0]:
            parameters.append({
                'ip_hostname': results_item_1[0],
                # context (artifact id) is added to associate results with the artifact
                'context': {'artifact_id': results_item_1[1]},
            })

    phantom.act(action="quarantine device", parameters=parameters, assets=['carbonblack'], name="quarantine_device_3", parent_action=action)

    return

def on_finish(container, summary):
    phantom.debug('on_finish() called')
    # This function is called after all actions are completed.
    # summary of all the action and/or all details of actions
    # can be collected here.

    # summary_json = phantom.get_summary()
    # if 'result' in summary_json:
        # for action_result in summary_json['result']:
            # if 'action_run_id' in action_result:
                # action_results = phantom.get_action_results(action_run_id=action_result['action_run_id'], result_data=False, flatten=False)
                # phantom.debug(action_results)

    return