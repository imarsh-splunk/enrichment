"""
"""

import phantom.rules as phantom
import json
from datetime import datetime, timedelta
def on_start(container):
    phantom.debug('on_start() called')
    
    # call 'check_for_disable' block
    check_for_disable(container=container)

    return

def disable_user_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('disable_user_1() called')
        
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'disable_user_1' call
    custom_function_results_data_1 = phantom.collect2(container=container, datapath=['cf_escu_list_merge_dedup_1:custom_function_result.data.*.item'], action_results=results)

    parameters = []
    
    # build parameters list for 'disable_user_1' call
    for custom_function_results_item_1 in custom_function_results_data_1:
        if custom_function_results_item_1[0]:
            parameters.append({
                'username': custom_function_results_item_1[0],
            })

    phantom.act(action="disable user", parameters=parameters, assets=['ldap'], name="disable_user_1")

    return

def credentials_check(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('credentials_check() called')

    # check for 'if' condition 1
    matched = phantom.decision(
        container=container,
        conditions=[
            ["filtered-data:filter_disable_artifacts:condition_1:artifact:*.cef.destinationUserId", "!=", ""],
            ["filtered-data:filter_disable_artifacts:condition_1:artifact:*.cef.destinationUserName", "!=", ""],
            ["filtered-data:filter_disable_artifacts:condition_1:artifact:*.cef.duser", "!=", ""],
            ["filtered-data:filter_disable_artifacts:condition_1:artifact:*.cef.sourceUserId", "!=", ""],
            ["filtered-data:filter_disable_artifacts:condition_1:artifact:*.cef.sourceUserName", "!=", ""],
            ["artifact:*.cef.suser", "!=", ""],
        ],
        logical_operator='or')

    # call connected blocks if condition 1 matched
    if matched:
        filter_credentials(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)
        return

    # call connected blocks for 'else' condition 2
    join_missing_data_comment(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)

    return

def missing_data_comment(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('missing_data_comment() called')

    phantom.comment(container=container, comment="Missing user credential information to disable account(s)")

    return

def join_missing_data_comment(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None):
    phantom.debug('join_missing_data_comment() called')

    # no callbacks to check, call connected block "missing_data_comment"
    phantom.save_run_data(key='join_missing_data_comment_called', value='missing_data_comment', auto=True)

    missing_data_comment(container=container, handle=handle)
    
    return

def filter_credentials(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('filter_credentials() called')

    # collect filtered artifact ids for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        conditions=[
            ["artifact:*.cef.destinationUserId", "not in", "custom_list:bogon_list"],
            ["artifact:*.cef.destinationUserName", "not in", "custom_list:bogon_list"],
            ["artifact:*.cef.duser", "not in", "custom_list:bogon_list"],
            ["artifact:*.cef.sourceUserId", "not in", "custom_list:bogon_list"],
            ["artifact:*.cef.sourceUserName", "not in", "custom_list:bogon_list"],
            ["artifact:*.cef.suser", "not in", "custom_list:bogon_list"],
        ],
        logical_operator='or',
        name="filter_credentials:condition_1")

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        cf_escu_list_merge_dedup_1(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

    return

def cf_escu_list_merge_dedup_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('cf_escu_list_merge_dedup_1() called')
    
    filtered_artifacts_data_0 = phantom.collect2(container=container, datapath=['filtered-data:filter_credentials:condition_1:artifact:*.cef.destinationUserId', 'filtered-data:filter_credentials:condition_1:artifact:*.cef.destinationUserName', 'filtered-data:filter_credentials:condition_1:artifact:*.cef.duser', 'filtered-data:filter_credentials:condition_1:artifact:*.cef.sourceUserId', 'filtered-data:filter_credentials:condition_1:artifact:*.cef.sourceUserName', 'filtered-data:filter_credentials:condition_1:artifact:*.cef.suser'])

    parameters = []

    filtered_artifacts_data_0_0 = [item[0] for item in filtered_artifacts_data_0]
    filtered_artifacts_data_0_1 = [item[1] for item in filtered_artifacts_data_0]
    filtered_artifacts_data_0_2 = [item[2] for item in filtered_artifacts_data_0]
    filtered_artifacts_data_0_3 = [item[3] for item in filtered_artifacts_data_0]
    filtered_artifacts_data_0_4 = [item[4] for item in filtered_artifacts_data_0]
    filtered_artifacts_data_0_5 = [item[5] for item in filtered_artifacts_data_0]

    parameters.append({
        'input_1': filtered_artifacts_data_0_0,
        'input_2': filtered_artifacts_data_0_1,
        'input_3': filtered_artifacts_data_0_2,
        'input_4': filtered_artifacts_data_0_3,
        'input_5': filtered_artifacts_data_0_4,
        'input_6': filtered_artifacts_data_0_5,
        'input_7': None,
        'input_8': None,
        'input_9': None,
        'input_10': None,
    })
    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################    

    # call custom function "escu/list_merge_dedup", returns the custom_function_run_id
    phantom.custom_function(custom_function='escu/list_merge_dedup', parameters=parameters, name='cf_escu_list_merge_dedup_1', callback=disable_user_1)

    return

def check_for_disable(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('check_for_disable() called')

    # check for 'if' condition 1
    matched = phantom.decision(
        container=container,
        conditions=[
            ["disable", "in", "artifact:*.tags"],
        ])

    # call connected blocks if condition 1 matched
    if matched:
        filter_disable_artifacts(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)
        return

    # call connected blocks for 'else' condition 2
    join_missing_data_comment(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)

    return

def filter_disable_artifacts(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('filter_disable_artifacts() called')

    # collect filtered artifact ids for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        conditions=[
            ["disable", "in", "artifact:*.tags"],
        ],
        name="filter_disable_artifacts:condition_1")

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        credentials_check(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

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