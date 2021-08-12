"""
"""

import phantom.rules as phantom
import json
from datetime import datetime, timedelta
def on_start(container):
    phantom.debug('on_start() called')
    
    # call 'checks_tags' block
    checks_tags(container=container)

    return

def check_for_network_indicators(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('check_for_network_indicators() called')

    # check for 'if' condition 1
    matched = phantom.decision(
        container=container,
        conditions=[
            ["filtered-data:filter_indicators:condition_1:artifact:*.cef.destinationAddress", "not in", "custom_list:bogon_list"],
            ["filtered-data:filter_indicators:condition_1:artifact:*.cef.destinationDnsDomain", "not in", "custom_list:bogon_list"],
            ["filtered-data:filter_indicators:condition_1:artifact:*.cef.sourceAddress", "not in", "custom_list:bogon_list"],
            ["filtered-data:filter_indicators:condition_1:artifact:*.cef.sourceDnsDomain", "not in", "custom_list:bogon_list"],
            ["filtered-data:filter_indicators:condition_1:artifact:*.cef.requestURL", "not in", "custom_list:bogon_list"],
            ["filtered-data:filter_indicators:condition_1:artifact:*.cef.url", "not in", "custom_list:bogon_list"],
            ["filtered-data:filter_indicators:condition_1:artifact:*.cef.dest_ip", "not in", "custom_list:bogon_list"],
            ["filtered-data:filter_indicators:condition_1:artifact:*.cef.src_ip", "not in", "custom_list:bogon_list"],
            ["filtered-data:filter_indicators:condition_1:artifact:*.cef.domain", "not in", "custom_list:bogon_list"],
        ],
        logical_operator='or')

    # call connected blocks if condition 1 matched
    if matched:
        filters_indator_by_type(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)
        return

    # call connected blocks for 'else' condition 2
    missing_artifacts(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)

    return

def checks_tags(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('checks_tags() called')

    # check for 'if' condition 1
    matched = phantom.decision(
        container=container,
        conditions=[
            ["blocking", "in", "artifact:*.tags"],
        ])

    # call connected blocks if condition 1 matched
    if matched:
        filter_indicators(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)
        return

    # call connected blocks for 'else' condition 2
    Missing_blocking_tag(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)

    return

def filter_indicators(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('filter_indicators() called')

    # collect filtered artifact ids for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        conditions=[
            ["blocking", "in", "artifact:*.tags"],
        ],
        name="filter_indicators:condition_1")

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        check_for_network_indicators(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

    return

def block_urls(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('block_urls() called')
        
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'block_urls' call
    filtered_artifacts_data_1 = phantom.collect2(container=container, datapath=['filtered-data:filters_indator_by_type:condition_3:artifact:*.cef.requestURL', 'filtered-data:filters_indator_by_type:condition_3:artifact:*.id'])

    parameters = []
    
    # build parameters list for 'block_urls' call
    for filtered_artifacts_item_1 in filtered_artifacts_data_1:
        if filtered_artifacts_item_1[0]:
            parameters.append({
                'url': filtered_artifacts_item_1[0],
                'url_category': "CustomBlockList",
                # context (artifact id) is added to associate results with the artifact
                'context': {'artifact_id': filtered_artifacts_item_1[1]},
            })

    phantom.act(action="block url", parameters=parameters, assets=['zscaler'], callback=join_check_ip_status, name="block_urls")

    return

def filters_indator_by_type(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('filters_indator_by_type() called')

    # collect filtered artifact ids for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        conditions=[
            ["filtered-data:filter_indicators:condition_1:artifact:*.cef.destinationAddress", "not in", "custom_list:bogon_list"],
            ["filtered-data:filter_indicators:condition_1:artifact:*.cef.sourceAddress", "not in", "custom_list:bogon_list"],
            ["filtered-data:filter_indicators:condition_1:artifact:*.cef.dest_ip", "not in", "custom_list:bogon_list"],
            ["artifact:*.cef.src_ip", "not in", "custom_list:bogon_list"],
        ],
        logical_operator='or',
        name="filters_indator_by_type:condition_1")

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        dedup_ips(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

    # collect filtered artifact ids for 'if' condition 2
    matched_artifacts_2, matched_results_2 = phantom.condition(
        container=container,
        conditions=[
            ["filtered-data:filter_indicators:condition_1:artifact:*.cef.destinationDnsDomain", "not in", "custom_list:bogon_list"],
            ["filtered-data:filter_indicators:condition_1:artifact:*.cef.sourceDnsDomain", "not in", "custom_list:bogon_list"],
            ["filtered-data:filter_indicators:condition_1:artifact:*.cef.domain", "not in", "custom_list:bogon_list"],
        ],
        logical_operator='and',
        name="filters_indator_by_type:condition_2")

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_2 or matched_results_2:
        dedup_domains(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function, filtered_artifacts=matched_artifacts_2, filtered_results=matched_results_2)

    # collect filtered artifact ids for 'if' condition 3
    matched_artifacts_3, matched_results_3 = phantom.condition(
        container=container,
        conditions=[
            ["filtered-data:filter_indicators:condition_1:artifact:*.cef.requestURL", "not in", ""],
            ["filtered-data:filter_indicators:condition_1:artifact:*.cef.url", "not in", ""],
        ],
        logical_operator='and',
        name="filters_indator_by_type:condition_3")

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_3 or matched_results_3:
        dedup_urls(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function, filtered_artifacts=matched_artifacts_3, filtered_results=matched_results_3)

    return

def update_url_artifact_tags(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('update_url_artifact_tags() called')
        
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'update_url_artifact_tags' call
    filtered_artifacts_data_1 = phantom.collect2(container=container, datapath=['filtered-data:filters_indator_by_type:condition_3:artifact:*.id', 'filtered-data:filters_indator_by_type:condition_3:artifact:*.id'])

    parameters = []
    
    # build parameters list for 'update_url_artifact_tags' call
    for filtered_artifacts_item_1 in filtered_artifacts_data_1:
        if filtered_artifacts_item_1[0]:
            parameters.append({
                'artifact_id': filtered_artifacts_item_1[0],
                'add_tags': "blocked",
                'remove_tags': "blocking",
                # context (artifact id) is added to associate results with the artifact
                'context': {'artifact_id': filtered_artifacts_item_1[1]},
            })

    phantom.act(action="update artifact tags", parameters=parameters, assets=['phantom'], name="update_url_artifact_tags", parent_action=action)

    return

def block_domains(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('block_domains() called')
        
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'block_domains' call
    custom_function_results_data_1 = phantom.collect2(container=container, datapath=['dedup_domains:custom_function_result.data.*.item'], action_results=results)

    parameters = []
    
    # build parameters list for 'block_domains' call
    for custom_function_results_item_1 in custom_function_results_data_1:
        if custom_function_results_item_1[0]:
            parameters.append({
                'domain': custom_function_results_item_1[0],
                'disable_safeguards': False,
            })

    phantom.act(action="block domain", parameters=parameters, assets=['umbrella'], callback=join_check_ip_status, name="block_domains")

    return

def dedup_domains(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('dedup_domains() called')
    
    filtered_artifacts_data_0 = phantom.collect2(container=container, datapath=['filtered-data:filters_indator_by_type:condition_2:artifact:*.cef.destinationDnsDomain', 'filtered-data:filters_indator_by_type:condition_2:artifact:*.cef.sourceDnsDomain', 'filtered-data:filters_indator_by_type:condition_2:artifact:*.cef.domain'])

    parameters = []

    filtered_artifacts_data_0_0 = [item[0] for item in filtered_artifacts_data_0]
    filtered_artifacts_data_0_1 = [item[1] for item in filtered_artifacts_data_0]
    filtered_artifacts_data_0_2 = [item[2] for item in filtered_artifacts_data_0]

    parameters.append({
        'input_1': filtered_artifacts_data_0_0,
        'input_2': filtered_artifacts_data_0_1,
        'input_3': filtered_artifacts_data_0_2,
        'input_4': None,
        'input_5': None,
        'input_6': None,
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

    # call custom function "ps-playbooks-dev/list_merge_dedup", returns the custom_function_run_id
    phantom.custom_function(custom_function='ps-playbooks-dev/list_merge_dedup', parameters=parameters, name='dedup_domains', callback=block_domains)

    return

def update_domain_artifact_tags(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('update_domain_artifact_tags() called')
        
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'update_domain_artifact_tags' call
    filtered_artifacts_data_1 = phantom.collect2(container=container, datapath=['filtered-data:filters_indator_by_type:condition_2:artifact:*.id', 'filtered-data:filters_indator_by_type:condition_2:artifact:*.id'])

    parameters = []
    
    # build parameters list for 'update_domain_artifact_tags' call
    for filtered_artifacts_item_1 in filtered_artifacts_data_1:
        if filtered_artifacts_item_1[0]:
            parameters.append({
                'artifact_id': filtered_artifacts_item_1[0],
                'add_tags': "blocked",
                'remove_tags': "blocking",
                # context (artifact id) is added to associate results with the artifact
                'context': {'artifact_id': filtered_artifacts_item_1[1]},
            })

    phantom.act(action="update artifact tags", parameters=parameters, assets=['phantom'], name="update_domain_artifact_tags")

    return

def dedup_ips(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('dedup_ips() called')
    
    filtered_artifacts_data_0 = phantom.collect2(container=container, datapath=['filtered-data:filters_indator_by_type:condition_1:artifact:*.cef.dest_ip', 'filtered-data:filters_indator_by_type:condition_1:artifact:*.cef.destinationAddress', 'filtered-data:filters_indator_by_type:condition_1:artifact:*.cef.src_ip', 'filtered-data:filters_indator_by_type:condition_1:artifact:*.cef.sourceAddress'])

    parameters = []

    filtered_artifacts_data_0_0 = [item[0] for item in filtered_artifacts_data_0]
    filtered_artifacts_data_0_1 = [item[1] for item in filtered_artifacts_data_0]
    filtered_artifacts_data_0_2 = [item[2] for item in filtered_artifacts_data_0]
    filtered_artifacts_data_0_3 = [item[3] for item in filtered_artifacts_data_0]

    parameters.append({
        'input_1': filtered_artifacts_data_0_0,
        'input_2': filtered_artifacts_data_0_1,
        'input_3': filtered_artifacts_data_0_2,
        'input_4': filtered_artifacts_data_0_3,
        'input_5': None,
        'input_6': None,
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

    # call custom function "ps-playbooks-dev/list_merge_dedup", returns the custom_function_run_id
    phantom.custom_function(custom_function='ps-playbooks-dev/list_merge_dedup', parameters=parameters, name='dedup_ips', callback=block_ip)

    return

def dedup_urls(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('dedup_urls() called')
    
    filtered_artifacts_data_0 = phantom.collect2(container=container, datapath=['filtered-data:filters_indator_by_type:condition_3:artifact:*.cef.requestURL', 'filtered-data:filters_indator_by_type:condition_3:artifact:*.cef.url'])

    parameters = []

    filtered_artifacts_data_0_0 = [item[0] for item in filtered_artifacts_data_0]
    filtered_artifacts_data_0_1 = [item[1] for item in filtered_artifacts_data_0]

    parameters.append({
        'input_1': filtered_artifacts_data_0_0,
        'input_2': filtered_artifacts_data_0_1,
        'input_3': None,
        'input_4': None,
        'input_5': None,
        'input_6': None,
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

    # call custom function "ps-playbooks-dev/list_merge_dedup", returns the custom_function_run_id
    phantom.custom_function(custom_function='ps-playbooks-dev/list_merge_dedup', parameters=parameters, name='dedup_urls', callback=block_urls)

    return

def block_ip(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('block_ip() called')
        
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'block_ip' call
    custom_function_results_data_1 = phantom.collect2(container=container, datapath=['dedup_ips:custom_function_result.data.*.item'], action_results=results)

    parameters = []
    
    # build parameters list for 'block_ip' call
    for custom_function_results_item_1 in custom_function_results_data_1:
        if custom_function_results_item_1[0]:
            parameters.append({
                'ip': custom_function_results_item_1[0],
                'url_category': "CustomBlockList",
            })

    phantom.act(action="block ip", parameters=parameters, assets=['zscaler'], callback=join_check_ip_status, name="block_ip")

    return

def check_ip_status(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('check_ip_status() called')

    # check for 'if' condition 1
    matched = phantom.decision(
        container=container,
        action_results=results,
        conditions=[
            ["block_ip:action_result.status", "==", "success"],
        ])

    # call connected blocks if condition 1 matched
    if matched:
        update_ip_artifact_tags(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)
        return

    # check for 'elif' condition 2
    matched = phantom.decision(
        container=container,
        action_results=results,
        conditions=[
            ["block_domains:action_result.status", "==", "success"],
        ])

    # call connected blocks if condition 2 matched
    if matched:
        update_domain_artifact_tags(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)
        return

    # check for 'elif' condition 3
    matched = phantom.decision(
        container=container,
        action_results=results,
        conditions=[
            ["block_urls:action_result.status", "==", "success"],
        ])

    # call connected blocks if condition 3 matched
    if matched:
        update_url_artifact_tags(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)
        return

    # call connected blocks for 'else' condition 4
    comment_and_pin_error(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)

    return

def join_check_ip_status(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None):
    phantom.debug('join_check_ip_status() called')
    
    # if the joined function has already been called, do nothing
    if phantom.get_run_data(key='join_check_ip_status_called'):
        return

    # no callbacks to check, call connected block "check_ip_status"
    phantom.save_run_data(key='join_check_ip_status_called', value='check_ip_status', auto=True)

    check_ip_status(container=container, handle=handle)
    
    return

def update_ip_artifact_tags(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('update_ip_artifact_tags() called')
        
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'update_ip_artifact_tags' call
    filtered_artifacts_data_1 = phantom.collect2(container=container, datapath=['filtered-data:filters_indator_by_type:condition_1:artifact:*.id', 'filtered-data:filters_indator_by_type:condition_1:artifact:*.id'])

    parameters = []
    
    # build parameters list for 'update_ip_artifact_tags' call
    for filtered_artifacts_item_1 in filtered_artifacts_data_1:
        if filtered_artifacts_item_1[0]:
            parameters.append({
                'artifact_id': filtered_artifacts_item_1[0],
                'add_tags': "blocked",
                'remove_tags': "blocking",
                # context (artifact id) is added to associate results with the artifact
                'context': {'artifact_id': filtered_artifacts_item_1[1]},
            })

    phantom.act(action="update artifact tags", parameters=parameters, assets=['phantom'], name="update_ip_artifact_tags")

    return

def comment_and_pin_error(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('comment_and_pin_error() called')

    phantom.comment(container=container, comment="There was an error with the blocking process. Please validate")

    phantom.pin(container=container, data="Check Blocking Actions", message="A blocking action failed", name=None)

    return

def Missing_blocking_tag(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('Missing_blocking_tag() called')

    phantom.comment(container=container, comment="Missing blocking tag on artifacts to be blocked")

    return

def missing_artifacts(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('missing_artifacts() called')

    phantom.comment(container=container, comment="Blocking tags were present, but no artifacts were selected. Review artifact and playbook decision and filter.")

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