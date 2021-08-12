"""
Cluster Load test playbook
"""

import phantom.rules as phantom
import json
from datetime import datetime, timedelta
##############################
# Start - Global Code Block

import time
from datetime import datetime, date, time, timedelta
import dateutil.relativedelta
import random

# End - Global Code block
##############################

def on_start(container):
    phantom.debug('on_start() called')
    
    # call 'Open_Event' block
    Open_Event(container=container)

    return

def Open_Event(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('Open_Event() called')
    phantom.set_status(container=container, status="open")
    run_queries(container=container)

    return

def fisma_filter(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('fisma_filter() called')

    # collect filtered artifact ids for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        action_results=results,
        conditions=[
            ["custom_join:custom_function:fisma_id", "==", "not found"],
        ],
        name="fisma_filter:condition_1")

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        quarantine_fisma_fail(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

    return

def vul_filter(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('vul_filter() called')

    # collect filtered artifact ids for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        action_results=results,
        conditions=[
            ["custom_join:custom_function:fisma_id", "!=", "not found"],
            ["custom_join:custom_function:vul_scan_end_timestamp", "==", "not found"],
        ],
        logical_operator='and',
        name="vul_filter:condition_1")

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        remediate_vul_none(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

    # collect filtered artifact ids for 'if' condition 2
    matched_artifacts_2, matched_results_2 = phantom.condition(
        container=container,
        action_results=results,
        conditions=[
            ["custom_join:custom_function:fisma_id", "!=", "not found"],
            ["custom_join:custom_function:vul_scan_end_timestamp", "!=", "not found"],
        ],
        logical_operator='and',
        name="vul_filter:condition_2")

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_2 or matched_results_2:
        vul_scan_seven_day_check(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_2, filtered_results=matched_results_2)

    return

def swam_filter(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('swam_filter() called')

    # collect filtered artifact ids for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        action_results=results,
        conditions=[
            ["custom_join:custom_function:fisma_id", "!=", "not found"],
            ["custom_join:custom_function:vul_scan_end_timestamp", "!=", "not found"],
            ["custom_join:custom_function:bigfix_last_seen", "==", "not found"],
            ["artifact:*.cef.deviceClassification", "==", "swam_manageable"],
        ],
        logical_operator='and',
        name="swam_filter:condition_1")

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        remediate_swam_fail(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

    # collect filtered artifact ids for 'if' condition 2
    matched_artifacts_2, matched_results_2 = phantom.condition(
        container=container,
        action_results=results,
        conditions=[
            ["custom_join:custom_function:fisma_id", "!=", "not found"],
            ["custom_join:custom_function:vul_scan_end_timestamp", "!=", "not found"],
            ["custom_join:custom_function:bigfix_last_seen", "!=", "not found"],
            ["artifact:*.cef.deviceClassification", "==", "swam_manageable"],
            ["vul_scan_seven_day_check:custom_function:date_offset", "==", True],
        ],
        logical_operator='and',
        name="swam_filter:condition_2")

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_2 or matched_results_2:
        allow_swam_pass(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_2, filtered_results=matched_results_2)

    return

def join_swam_filter(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('join_swam_filter() called')
    
    # if the joined function has already been called, do nothing
    if phantom.get_run_data(key='join_swam_filter_called'):
        return

    # check if all connected incoming actions are done i.e. have succeeded or failed
    if phantom.actions_done([ 'run_queries' ]):
        
        # save the state that the joined function has now been called
        phantom.save_run_data(key='join_swam_filter_called', value='swam_filter')
        
        # call connected block "swam_filter"
        swam_filter(container=container, handle=handle)
    
    return

def vul_date_filter(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('vul_date_filter() called')

    # collect filtered artifact ids for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        action_results=results,
        conditions=[
            ["vul_scan_seven_day_check:custom_function:date_offset", "==", False],
        ],
        name="vul_date_filter:condition_1")

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        remediate_vul_fail(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

    # collect filtered artifact ids for 'if' condition 2
    matched_artifacts_2, matched_results_2 = phantom.condition(
        container=container,
        action_results=results,
        conditions=[
            ["vul_scan_seven_day_check:custom_function:date_offset", "==", True],
            ["artifact:*.cef.deviceClassification", "==", "swam_unmanageable"],
        ],
        logical_operator='and',
        name="vul_date_filter:condition_2")

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_2 or matched_results_2:
        allow_swam_none(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_2, filtered_results=matched_results_2)

    # collect filtered artifact ids for 'if' condition 3
    matched_artifacts_3, matched_results_3 = phantom.condition(
        container=container,
        action_results=results,
        conditions=[
            ["vul_scan_seven_day_check:custom_function:date_offset", "==", True],
            ["artifact:*.cef.deviceClassification", "==", "swam_manageable"],
        ],
        logical_operator='and',
        name="vul_date_filter:condition_3")

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_3 or matched_results_3:
        join_swam_filter(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_3, filtered_results=matched_results_3)

    return

def quarantine_fisma_fail(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('quarantine_fisma_fail() called')

    phantom.add_tags(container=container, tags="quarantine_fisma_fail")

    return

def remediate_vul_none(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('remediate_vul_none() called')

    phantom.add_tags(container=container, tags="remediate_vul_none")

    return

def remediate_vul_fail(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('remediate_vul_fail() called')

    phantom.add_tags(container=container, tags="remediate_vul_fail")

    return

def allow_swam_none(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('allow_swam_none() called')

    phantom.add_tags(container=container, tags="allow_swam_none")

    return

def remediate_swam_fail(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('remediate_swam_fail() called')

    phantom.add_tags(container=container, tags="remediate_swam_fail")

    return

def allow_swam_pass(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('allow_swam_pass() called')

    phantom.add_tags(container=container, tags="allow_swam_pass")

    return

def run_queries(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('run_queries() called')
    
    # collect data for 'run_queries' call
    # parameter list for template variable replacement
    datapaths = [
        "artifact:*.cef.deviceAddress",
        "artifact:*.cef.deviceMacAddress",
    ]
    device_address, device_mac_address = phantom.collect2(container=container, datapath=datapaths)[0]
    
    phantom.debug("{} {}".format(device_address, device_mac_address))
    
    # Build FISMA query
    query_fisma = "| inputlookup asset_lookup.csv | search ip={0} mac={1} | head 1 | fields fisma_id | stats values(fisma_id) as fisma_id".format(device_address, device_mac_address)

    # Build BigFixQuery
    query_bigfix = "| pivot CDM_HWAM BigFix_HWAM latest(last_seen) AS last_seen FILTER ip is {0} FILTER mac is {1} ROWSUMMARY 0 COLSUMMARY 0 NUMCOLS 0 SHOWOTHER 1".format(device_address, device_mac_address)

    # Build Vul Scan Query
    phantom.debug('Format_Vul_Scan_Query ')
    offset_days = 7
    d = datetime.today() - timedelta(days=offset_days)
    utc_time = datetime.strptime(str(d),"%Y-%m-%d %H:%M:%S.%f")
    current_ts_with_offset = str((utc_time - datetime(1970, 1, 1)).total_seconds())
    phantom.debug(current_ts_with_offset)
    
    template_p1 = """| tstats latest(VSR_CVE.host_federated) AS host_federated latest(host) AS host latest(VSR_CVE.scan_subject_fqdn) AS fqdn max(VSR_CVE.scan_end_timestamp) AS scan_end_timestamp from datamodel=CDM_VUL
 where (_time > """
    template_p2 =""", VSR_CVE.scan_subject=\"{0}\" ) groupby VSR_CVE.scan_subject
| rename VSR_CVE.scan_subject as ipv4 
| search ipv4=\"{0}\"
| lookup temporal_asset_lookup.csv ip as ipv4 OUTPUTNEW _key as latest_device_id, mac
| where (mac == \"{1}\")
| head 1"""
    
    query_vuln_scan = (template_p1+current_ts_with_offset+template_p2).format(device_address, device_mac_address)
    #formatted_data_1 = phantom.get_format_data(name='Format_FISMA_Query')
    #formatted_data_2 = phantom.get_format_data(name='Format_Vul_Scan_Query')
    #formatted_data_3 = phantom.get_format_data(name='Format_BigFix_Query')

    parameters = [{
        'query': query_fisma,
        #'display': "",
    },
    {
        'query': query_vuln_scan,
        #'display': "",
    },
    {
        'query': query_bigfix,
        #'display': "",
    }]
    
    #splunk_node_assets = ['splunk10-10-1', 'splunk10-10-2', 'splunk10-10-3', 'splunk10-10-4', 'splunk10-10-5', 'splunk10-10-6', 'splunk10-10-7', 'splunk10-10-8', 'splunk10-10-9', 'splunk10-10-10']
    #asset_choice = []
    #asset_choice.append(random.choice(splunk_node_assets))
    asset_choice = ['splunk_nac']
    phantom.act("run query", parameters=parameters, assets=asset_choice, callback=custom_join, name="run_queries")
    return

"""
Check the splunk query statuses to make sure they are all finished. Use the string "custom_join_queries_done" as a save_run_data key to only continue if all queries are finished, and to stop this thread of execution if we have already continued past it at least once, or if the searches aren't ready yet.
"""
def custom_join(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('custom_join() called')
    results_data_1 = phantom.collect2(container=container, datapath=['run_queries:action_result.parameter.query', 'run_queries:action_result.status', 'run_queries:action_result.data.*.fisma_id', 'run_queries:action_result.data.*.scan_end_timestamp', 'run_queries:action_result.data.*.last_seen'], action_results=results)
    results_item_1_0 = [item[0] for item in results_data_1]
    results_item_1_1 = [item[1] for item in results_data_1]
    results_item_1_2 = [item[2] for item in results_data_1]
    results_item_1_3 = [item[3] for item in results_data_1]
    results_item_1_4 = [item[4] for item in results_data_1]

    custom_join__fisma_id = None
    custom_join__vul_scan_end_timestamp = None
    custom_join__bigfix_last_seen = None

    ################################################################################
    ## Custom Code Start
    ################################################################################

    phantom.debug("custom_join_queries_done: {}".format(phantom.get_run_data(key="custom_join_queries_done")))
    if phantom.get_run_data(key="custom_join_queries_done") == "done":
        phantom.debug("another callback reached here already and moved on, so leaving custom_join() early")
        return

    phantom.debug("queries: {}".format(results_item_1_0))
    
    phantom.debug("status: {}".format(results_item_1_1))
    if results_item_1_1 != ['success', 'success', 'success']:
        phantom.debug("either a splunk query failed or one is still running, so leaving custom_join() early")
        return
    else:
        phantom.save_run_data(key="custom_join_queries_done", value="done")

    phantom.debug("fisma_id: {}".format(results_item_1_2))
    custom_join__fisma_id = "not found"
    for item in results_item_1_2:
        if item:
            custom_join__fisma_id = item
    phantom.comment(container=container, comment=custom_join__fisma_id)

    phantom.debug("vul_scan_end_timestamp: {}".format(results_item_1_3))
    custom_join__vul_scan_end_timestamp = "not found"
    for item in results_item_1_3:
        if item:
            custom_join__vul_scan_end_timestamp = item
    phantom.comment(container=container, comment=custom_join__vul_scan_end_timestamp)

    phantom.debug("bigfix_last_seen: {}".format(results_item_1_4))
    custom_join__bigfix_last_seen = "not found"
    for item in results_item_1_4:
        if item:
            custom_join__bigfix_last_seen = item
    phantom.comment(container=container, comment=custom_join__bigfix_last_seen)

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key='custom_join:fisma_id', value=json.dumps(custom_join__fisma_id))
    phantom.save_run_data(key='custom_join:vul_scan_end_timestamp', value=json.dumps(custom_join__vul_scan_end_timestamp))
    phantom.save_run_data(key='custom_join:bigfix_last_seen', value=json.dumps(custom_join__bigfix_last_seen))
    fisma_filter(container=container)
    vul_filter(container=container)
    join_swam_filter(container=container)

    return

"""
Return True if the given timestamp is less than seven days ago, and False if it is more than or equal to seven days ago.
"""
def vul_scan_seven_day_check(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('vul_scan_seven_day_check() called')
    custom_join__vul_scan_end_timestamp = json.loads(phantom.get_run_data(key='custom_join:vul_scan_end_timestamp'))

    vul_scan_seven_day_check__date_offset = None

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # compute the difference in time between today and the last scan end time
    phantom.debug(custom_join__vul_scan_end_timestamp)
    scan_time = datetime.fromtimestamp(float(custom_join__vul_scan_end_timestamp))
    now = datetime.now()
    difference = dateutil.relativedelta.relativedelta(now, scan_time)
    difference_days = difference.days
    
    # if the difference is more than 7 days, return True
    phantom.debug("difference between now and given time in days: {}".format(difference_days))
    if difference_days < 7:
        vul_scan_seven_day_check__date_offset = True
    else:
        vul_scan_seven_day_check__date_offset = False

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key='vul_scan_seven_day_check:date_offset', value=json.dumps(vul_scan_seven_day_check__date_offset))
    vul_date_filter(container=container)

    return

def on_finish(container, summary):
    phantom.debug('on_finish() called')
    # This function is called after all actions are completed.
    # summary of all the action and/or all detals of actions
    # can be collected here.

    # summary_json = phantom.get_summary()
    # if 'result' in summary_json:
        # for action_result in summary_json['result']:
            # if 'action_run_id' in action_result:
                # action_results = phantom.get_action_results(action_run_id=action_result['action_run_id'], result_data=False, flatten=False)
                # phantom.debug(action_results)

    return