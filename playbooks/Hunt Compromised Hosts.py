"""
This playbook takes existing indicators and then searches Splunk to produce a list of other possible assets that have seen those indicators. These indicators are ip addresses, domains, urls, hashes and ssl hashs
"""

import phantom.rules as phantom
import json
from datetime import datetime, timedelta
##############################
# Start - Global Code Block

import time

# End - Global Code block
##############################

def on_start(container):
    phantom.debug('on_start() called')
    
    # call 'workbook_task_url' block
    workbook_task_url(container=container)

    return

"""
Needs threat_match_field and threat_match_value 
"""
def Check_for_threat_match_field(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('Check_for_threat_match_field() called')

    # check for 'if' condition 1
    matched = phantom.decision(
        container=container,
        action_results=results,
        conditions=[
            ["artifact:*.label", "!=", ""],
            ["get_workbook_task:action_result.data.*.response_body.data.*.status", "in", "2,0"],
        ],
        logical_operator='and')

    # call connected blocks if condition 1 matched
    if matched:
        task_url_format(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)
        return

    # check for 'elif' condition 2
    matched = phantom.decision(
        container=container,
        action_results=results,
        conditions=[
            ["artifact:*.label", "!=", ""],
            ["get_workbook_task:action_result.data.*.response_body.data.*.status", "==", 1],
        ],
        logical_operator='or')

    # call connected blocks if condition 2 matched
    if matched:
        standalone_hunt(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)
        return

    # call connected blocks for 'else' condition 3
    missing_artifacts(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)

    return

"""
threat_match_field=url
"""
def filter_url_or_ip_or_hash(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('filter_url_or_ip_or_hash() called')

    # collect filtered artifact ids for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        action_results=results,
        conditions=[
            ["filtered-data:filter_artifact_severity:condition_1:artifact:*.cef.requestURL", "!=", ""],
            ["filtered-data:filter_artifact_severity:condition_1:artifact:*.cef.url", "!=", ""],
            ["filtered-data:filter_artifact_severity:condition_1:artifact:*.cef.sourceDnsDomain", "!=", ""],
            ["filtered-data:filter_artifact_severity:condition_1:artifact:*.cef.sntdom", "!=", ""],
            ["filtered-data:filter_artifact_severity:condition_1:artifact:*.cef.destinationDnsDomain", "!=", ""],
            ["filtered-data:filter_artifact_severity:condition_1:artifact:*.cef.dntdom", "!=", ""],
        ],
        logical_operator='or',
        name="filter_url_or_ip_or_hash:condition_1")

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        merge_domains_urls(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

    # collect filtered artifact ids for 'if' condition 2
    matched_artifacts_2, matched_results_2 = phantom.condition(
        container=container,
        action_results=results,
        conditions=[
            ["filtered-data:filter_artifact_severity:condition_1:artifact:*.cef.destinationAddress", "!=", ""],
            ["filtered-data:filter_artifact_severity:condition_1:artifact:*.cef.dest_ip", "!=", ""],
            ["filtered-data:filter_artifact_severity:condition_1:artifact:*.cef.dest", "!=", ""],
            ["filtered-data:filter_artifact_severity:condition_1:artifact:*.cef.sourceAddress", "!=", ""],
            ["filtered-data:filter_artifact_severity:condition_1:artifact:*.cef.src", "!=", ""],
            ["filtered-data:filter_artifact_severity:condition_1:artifact:*.cef.src_ip", "!=", ""],
        ],
        logical_operator='or',
        name="filter_url_or_ip_or_hash:condition_2")

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_2 or matched_results_2:
        merge_ips(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function, filtered_artifacts=matched_artifacts_2, filtered_results=matched_results_2)

    # collect filtered artifact ids for 'if' condition 3
    matched_artifacts_3, matched_results_3 = phantom.condition(
        container=container,
        action_results=results,
        conditions=[
            ["filtered-data:filter_artifact_severity:condition_1:artifact:*.cef.fileHash", "!=", ""],
            ["filtered-data:filter_artifact_severity:condition_1:artifact:*.cef.fileHashMd5", "!=", ""],
            ["filtered-data:filter_artifact_severity:condition_1:artifact:*.cef.fileHashSha1", "!=", ""],
            ["filtered-data:filter_artifact_severity:condition_1:artifact:*.cef.fileHashSha256", "!=", ""],
            ["filtered-data:filter_artifact_severity:condition_1:artifact:*.cef.fileHashSha512", "!=", ""],
        ],
        logical_operator='or',
        name="filter_url_or_ip_or_hash:condition_3")

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_3 or matched_results_3:
        merge_hashes(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function, filtered_artifacts=matched_artifacts_3, filtered_results=matched_results_3)

    return

"""
Web.url
"""
def run_Web_query(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('run_Web_query() called')
        
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'run_Web_query' call
    formatted_data_1 = phantom.get_format_data(name='search_WEB_for_url_format')

    parameters = []
    
    # build parameters list for 'run_Web_query' call
    parameters.append({
        'query': formatted_data_1,
        'command': "",
        'display': "_time,src,dest,url,action,app,user",
        'parse_only': False,
    })

    phantom.act(action="run query", parameters=parameters, assets=['splunk personal'], callback=decision_6, name="run_Web_query")

    return

"""
ctime(_indextime - (3 * 24 * 60 * 60))

0 = index
"""
def calculate_day_earliest_time(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('calculate_day_earliest_time() called')
    
    container_data = phantom.collect2(container=container, datapath=['artifact:*.cef._indextime', 'artifact:*.id'])
    results_data_1 = phantom.collect2(container=container, datapath=['get_days_to_hunt_for:action_result.summary.responses.0'], action_results=results)
    container_item_0 = [item[0] for item in container_data]
    results_item_1_0 = [item[0] for item in results_data_1]

    calculate_day_earliest_time__earliest = None

    ################################################################################
    ## Custom Code Start
    ################################################################################
    calculate_day_earliest_time__earliest = []
        
    # set number of days (from prompt input) * hours * minutes * seconds (3 days)
    #phantom.debug(results_data_1[0][0])
    numberofseconds = (int(results_data_1[0][0]) * 24 * 60 * 60)
    phantom.debug("The number of days for offset {} and converted to seconds {}".format(results_data_1[0][0],numberofseconds))
    
    # check if we have any artifacts with _indextime 
    #phantom.debug(container_data)
    if not container_data[0][0]:
        # get current time
        current = time.time()
        earliest = current - numberofseconds
        phantom.debug("The current earliest time is {}, the latest is {} and the offset is {}".format(earliest,current,numberofseconds))

    else:
        # get _indextime
        indextime = int(container_data[0][0])
        phantom.debug(indextime)
        earliest = str(indextime - numberofseconds)
        phantom.debug("The index earliest time is {}, the latest is {} and the offset is {}".format(earliest,current,numberofseconds))

    calculate_day_earliest_time__earliest.insert(0,str(earliest))
    phantom.debug("Outputting earliest time: {}".format(calculate_day_earliest_time__earliest[0]))

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key='calculate_day_earliest_time:earliest', value=json.dumps(calculate_day_earliest_time__earliest))
    filter_artifact_severity(container=container)

    return

"""
Web.url
"""
def search_WEB_for_url_format(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('search_WEB_for_url_format() called')
    
    template = """| tstats count(\"web.url\") as count  FROM datamodel=Web WHERE web.url=\"*{0}*\" _time>{1} _time<{2} GROUPBY web.url, sourcetype, web.user, web.action, web.src, web.dest, web.app,_time
| rename web.url as url, web.user as user, web.src as src, web.dest as dest, web.app as app, web.action as action| fields _time,src,dest,url,action,app,user"""

    # parameter list for template variable replacement
    parameters = [
        "merge_domains_urls:custom_function_result.data.*.item",
        "calculate_day_earliest_time:custom_function:earliest",
        "filtered-data:filter_url_or_ip_or_hash:condition_1:artifact:*.cef._indextime",
    ]

    phantom.format(container=container, template=template, parameters=parameters, name="search_WEB_for_url_format")

    run_Web_query(container=container)

    return

def join_search_WEB_for_url_format(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None):
    phantom.debug('join_search_WEB_for_url_format() called')

    # check if all connected incoming playbooks, actions, or custom functions are done i.e. have succeeded or failed
    if phantom.completed(action_names=['run_EMAIL_query']):
        
        # call connected block "search_WEB_for_url_format"
        search_WEB_for_url_format(container=container, handle=handle)
    
    return

"""
Email.url
"""
def search_Email_url_format(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('search_Email_url_format() called')
    
    template = """| tstats  count as \"Count\" FROM datamodel=Email WHERE nodename=All_Email 
All_Email.url=\"{0}*\" _time>{1}  _time<{2} GROUPBY All_Email.file_hash, All_Email.src, All_Email.dest, sourcetype, _time span=auto, All_Email.url | fields - _span | rename All_Email.file_hash as file_hash, All_Email.src as src, All_Email.dest as dest, All_Email.url as url | fields + file_hash, src, dest, sourcetype, _time, url, Count"""

    # parameter list for template variable replacement
    parameters = [
        "merge_domains_urls:custom_function_result.data.*.item",
        "calculate_day_earliest_time:custom_function:earliest",
        "filtered-data:filter_url_or_ip_or_hash:condition_1:artifact:*.cef._indextime",
    ]

    phantom.format(container=container, template=template, parameters=parameters, name="search_Email_url_format")

    run_EMAIL_query(container=container)

    return

"""
Email.url
"""
def run_EMAIL_query(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('run_EMAIL_query() called')
        
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'run_EMAIL_query' call
    formatted_data_1 = phantom.get_format_data(name='search_Email_url_format')

    parameters = []
    
    # build parameters list for 'run_EMAIL_query' call
    parameters.append({
        'query': formatted_data_1,
        'command': "",
        'display': "_time, src, dest, sourcetype, file_hash, url,Count",
        'parse_only': False,
    })

    phantom.act(action="run query", parameters=parameters, assets=['splunk personal'], callback=Check_Number_of_URL_results, name="run_EMAIL_query")

    return

def search_EMAIL_hash_format(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('search_EMAIL_hash_format() called')
    
    template = """| tstats count FROM datamodel=Email WHERE nodename=All_Email All_Email.file_hash=\"{0}\"
_time>{1} _time<{2}  BY All_Email.file_hash,All_Email.src, All_Email.dest, sourcetype, _time span=auto, All_Email.url | rename All_Email.file_hash as file_hash, All_Email.src as src, All_Email.dest as dest, All_Email.url as url  | fields  _time, src, dest, sourcetype, file_hash, url, count"""

    # parameter list for template variable replacement
    parameters = [
        "merge_hashes:custom_function_result.data.*.item",
        "calculate_day_earliest_time:custom_function:earliest",
        "filtered-data:filter_url_or_ip_or_hash:condition_3:artifact:*.cef._indextime",
    ]

    phantom.format(container=container, template=template, parameters=parameters, name="search_EMAIL_hash_format")

    run_Email_Hash_query(container=container)

    return

def join_search_EMAIL_hash_format(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None):
    phantom.debug('join_search_EMAIL_hash_format() called')

    # check if all connected incoming playbooks, actions, or custom functions are done i.e. have succeeded or failed
    if phantom.completed(action_names=['run_File_Hash_Query']):
        
        # call connected block "search_EMAIL_hash_format"
        search_EMAIL_hash_format(container=container, handle=handle)
    
    return

def run_Email_Hash_query(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('run_Email_Hash_query() called')
        
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'run_Email_Hash_query' call
    formatted_data_1 = phantom.get_format_data(name='search_EMAIL_hash_format')

    parameters = []
    
    # build parameters list for 'run_Email_Hash_query' call
    parameters.append({
        'query': formatted_data_1,
        'command': "",
        'display': "_time, src, dest, sourcetype, file_hash, url, count",
        'parse_only': False,
    })

    phantom.act(action="run query", parameters=parameters, assets=['splunk personal'], callback=Check_results_for_email_hash, name="run_Email_Hash_query")

    return

def search_File_Hash_format(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('search_File_Hash_format() called')
    
    template = """| tstats count FROM datamodel=Endpoint.Filesystem WHERE Filesystem.file_hash=\"{0}\" _time>{1} _time<{2} GROUPBY _time,Filesystem.file_hash, Filesystem.dest, Filesystem.user, Filesystem.action,Filesystem.file_name ,Filesystem.file_create_time  | rename Filesystem.file_hash as file_hash,Filesystem.dest as dest, Filesystem.user as user, Filesystem.action as action, Filesystem.file_name as file_name,Filesystem.file_create_time as file_create_time 
| fields _time, dest,action,user,file_name,file_hash,file_create_time,count"""

    # parameter list for template variable replacement
    parameters = [
        "merge_hashes:custom_function_result.data.*.item",
        "calculate_day_earliest_time:custom_function:earliest",
        "filtered-data:filter_url_or_ip_or_hash:condition_3:artifact:*.cef._indextime",
    ]

    phantom.format(container=container, template=template, parameters=parameters, name="search_File_Hash_format")

    run_File_Hash_Query(container=container)

    return

def run_File_Hash_Query(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('run_File_Hash_Query() called')
        
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'run_File_Hash_Query' call
    formatted_data_1 = phantom.get_format_data(name='search_File_Hash_format')

    parameters = []
    
    # build parameters list for 'run_File_Hash_Query' call
    parameters.append({
        'query': formatted_data_1,
        'command': "",
        'display': "_time,dest,action,user,file_name,file_hash,file_create_time,count",
        'parse_only': False,
    })

    phantom.act(action="run query", parameters=parameters, assets=['splunk personal'], callback=Check_Number_of_File_Hash_Results, name="run_File_Hash_Query")

    return

def Format_Email_Hash_Results(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('Format_Email_Hash_Results() called')
    
    template = """Email Hash {2} Found in Splunk between  _time={0} and _indextime={1}
----
| _time  | src | dest  | sourcetype | file_hash | url | count |
| --- | --- | --- | --- | --- | --- | --- |
%%
| {3} | {4} | {5} |  {6} | {7} | {8}|  {9}
%%"""

    # parameter list for template variable replacement
    parameters = [
        "calculate_day_earliest_time:custom_function:earliest",
        "filtered-data:filter_url_or_ip_or_hash:condition_3:artifact:*.cef._indextime",
        "filtered-data:filter_url_or_ip_or_hash:condition_3:artifact:*.cef.threat_match_value",
        "run_Email_Hash_query:action_result.data.*._time",
        "run_Email_Hash_query:action_result.data.*.src",
        "run_Email_Hash_query:action_result.data.*.dest",
        "run_Email_Hash_query:action_result.data.*.sourcetype",
        "run_Email_Hash_query:action_result.data.*.file_hash",
        "run_Email_Hash_query:action_result.data.*.url",
        "run_Email_Hash_query:action_result.data.*.count",
    ]

    phantom.format(container=container, template=template, parameters=parameters, name="Format_Email_Hash_Results")

    join_Format_Final_Hash_Results(container=container)

    return

def Format_WebURL_results(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('Format_WebURL_results() called')
    
    template = """Web URL {2} Found in Splunk between  _time={0} and _indextime={1}
----
| _time  | src | dest  | url | action | app | user |
| --- | --- | --- | --- | --- | --- | --- |
%%
| {3} | {4} | {5} |  {6} |  
%%"""

    # parameter list for template variable replacement
    parameters = [
        "calculate_day_earliest_time:custom_function:earliest",
        "filtered-data:filter_url_or_ip_or_hash:condition_1:artifact:*.cef._indextime",
        "filtered-data:filter_url_or_ip_or_hash:condition_1:artifact:*.cef.threat_match_value",
        "run_Web_query:action_result.data.*._time",
        "run_Web_query:action_result.data.*.src",
        "run_Web_query:action_result.data.*.dest",
        "run_Web_query:action_result.data.*.action",
    ]

    phantom.format(container=container, template=template, parameters=parameters, name="Format_WebURL_results")

    join_Format_Final_URL_Results(container=container)

    return

def search_Network_Sessions_Format(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('search_Network_Sessions_Format() called')
    
    template = """| tstats count AS \"Count of All Sessions\" from datamodel=Network_Sessions where nodename = All_Sessions All_Sessions.dest_ip=\"{0}\" OR All_Sessions.src_ip=\"{0}\" _time>{1} _time<{2} BY _time, sourcetype, All_Sessions.user, All_Sessions.dest_ip, All_Sessions.src_ip | rename All_Sessions.user as user, All_Sessions.dest_ip as dest_ip, All_Sessions.src_ip as src_ip | fields + _time,sourcetype, user, dest_ip, src_ip, Count"""

    # parameter list for template variable replacement
    parameters = [
        "merge_ips:custom_function_result.data.*.item",
        "calculate_day_earliest_time:custom_function:earliest",
        "filtered-data:filter_url_or_ip_or_hash:condition_2:artifact:*.cef._indextime",
    ]

    phantom.format(container=container, template=template, parameters=parameters, name="search_Network_Sessions_Format")

    run_Network_Sessions_Query(container=container)

    return

def run_Network_Sessions_Query(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('run_Network_Sessions_Query() called')
        
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'run_Network_Sessions_Query' call
    formatted_data_1 = phantom.get_format_data(name='search_Network_Sessions_Format')

    parameters = []
    
    # build parameters list for 'run_Network_Sessions_Query' call
    parameters.append({
        'query': formatted_data_1,
        'command': "",
        'display': "_time,sourcetype, user, dest_ip, src_ip, Count",
        'parse_only': False,
    })

    phantom.act(action="run query", parameters=parameters, assets=['splunk personal'], callback=Check_Number_of_IP_Sessions_Results, name="run_Network_Sessions_Query")

    return

def search_Network_Traffic_format(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('search_Network_Traffic_format() called')
    
    template = """| tstats count as \"Count\" FROM datamodel=Network_Traffic WHERE  nodename=All_Traffic All_Traffic.dest_ip=\"{0}\"
OR  All_Traffic.src_ip=\"{0}\"  _time>{1} _time<{2} GROUPBY _time, sourcetype, All_Traffic.app, All_Traffic.action, All_Traffic.dest_ip, All_Traffic.src_ip, All_Traffic.user | rename All_Traffic.app as app, All_Traffic.action as action, All_Traffic.dest_ip as dest_ip, All_Traffic.src_ip as src_ip, All_Traffic.user as user | fields + _time, sourcetype, app, action, dest_ip, src_ip, user, Count"""

    # parameter list for template variable replacement
    parameters = [
        "merge_ips:custom_function_result.data.*.item",
        "calculate_day_earliest_time:custom_function:earliest",
        "filtered-data:filter_url_or_ip_or_hash:condition_2:artifact:*.cef._indextime",
    ]

    phantom.format(container=container, template=template, parameters=parameters, name="search_Network_Traffic_format")

    run_Network_Traffic_query(container=container)

    return

def join_search_Network_Traffic_format(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None):
    phantom.debug('join_search_Network_Traffic_format() called')

    # check if all connected incoming playbooks, actions, or custom functions are done i.e. have succeeded or failed
    if phantom.completed(action_names=['run_Network_Sessions_Query']):
        
        # call connected block "search_Network_Traffic_format"
        search_Network_Traffic_format(container=container, handle=handle)
    
    return

def run_Network_Traffic_query(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('run_Network_Traffic_query() called')
        
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'run_Network_Traffic_query' call
    formatted_data_1 = phantom.get_format_data(name='search_Network_Traffic_format')

    parameters = []
    
    # build parameters list for 'run_Network_Traffic_query' call
    parameters.append({
        'query': formatted_data_1,
        'command': "",
        'display': "_time, sourcetype, app, action, dest_ip, src_ip, user, Count",
        'parse_only': False,
    })

    phantom.act(action="run query", parameters=parameters, assets=['splunk personal'], callback=Check_for_Network_Traffic_Results, name="run_Network_Traffic_query")

    return

def Format_Network_Results(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('Format_Network_Results() called')
    
    template = """Network Traffic  for  Found in Splunk between  _time {0} and _indextime {1}
----
| _time  | sourcetype | app  | action | dest_ip | src_ip | user | Count
| --- | --- | --- | --- | --- | --- | --- |
%%
| {2}| {3} | {4} | {5} |  {6} | {7}| {8} | {9}
%%"""

    # parameter list for template variable replacement
    parameters = [
        "calculate_day_earliest_time:custom_function:earliest",
        "filtered-data:filter_url_or_ip_or_hash:condition_2:artifact:*.cef._indextime",
        "run_Network_Traffic_query:action_result.data.*._time",
        "run_Network_Traffic_query:action_result.data.*.sourcetype",
        "run_Network_Traffic_query:action_result.data.*.app",
        "run_Network_Traffic_query:action_result.data.*.action",
        "run_Network_Traffic_query:action_result.data.*.dest_ip",
        "run_Network_Traffic_query:action_result.data.*.src_ip",
        "run_Network_Traffic_query:action_result.data.*.user",
        "run_Network_Traffic_query:action_result.data.*.Count",
    ]

    phantom.format(container=container, template=template, parameters=parameters, name="Format_Network_Results")

    join_Format_Final_IP_Results(container=container)

    return

def Format_FileHash_events(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('Format_FileHash_events() called')
    
    template = """File Hash Found in Splunk between  _time{0} and _indextime {1} 
----
| _time  | dest | action  | user | file_name | file_create_time | count |
| --- | --- | --- | --- | --- | --- | --- |
%%
| {3} | {4} | {5} |  {6} | {7} | {8} 
%%
---
SPL
`{9}`"""

    # parameter list for template variable replacement
    parameters = [
        "calculate_day_earliest_time:custom_function:earliest",
        "run_File_Hash_Query:artifact:*.cef._indextime",
        "run_File_Hash_Query:action_result.data.*._time",
        "run_File_Hash_Query:action_result.data.*.dest",
        "run_File_Hash_Query:action_result.data.*.action",
        "run_File_Hash_Query:action_result.data.*.user",
        "run_File_Hash_Query:action_result.data.*.file_name",
        "run_File_Hash_Query:action_result.data.*.file_create_time",
        "run_File_Hash_Query:action_result.data.*.count",
        "run_File_Hash_Query:action_result.parameter.command",
    ]

    phantom.format(container=container, template=template, parameters=parameters, name="Format_FileHash_events")

    join_search_EMAIL_hash_format(container=container)

    return

def Check_Number_of_File_Hash_Results(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('Check_Number_of_File_Hash_Results() called')

    # check for 'if' condition 1
    matched = phantom.decision(
        container=container,
        action_results=results,
        conditions=[
            ["run_File_Hash_Query:action_result.summary.total_events", ">", 0],
        ])

    # call connected blocks if condition 1 matched
    if matched:
        Format_FileHash_events(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)
        return

    # call connected blocks for 'else' condition 2
    Format_No_FileHash_Format(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)

    return

def Format_No_FileHash_Format(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('Format_No_FileHash_Format() called')
    
    template = """No Matching {2} File Hash Found in Splunk between  _time={0} and _indextime={1}

SPL
`{3}`"""

    # parameter list for template variable replacement
    parameters = [
        "calculate_day_earliest_time:custom_function:earliest",
        "artifact:*.cef._indextime",
        "artifact:*.cef.threat_match_value",
        "run_File_Hash_Query:action_result.parameter.command",
    ]

    phantom.format(container=container, template=template, parameters=parameters, name="Format_No_FileHash_Format")

    join_search_EMAIL_hash_format(container=container)

    return

def Check_results_for_email_hash(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('Check_results_for_email_hash() called')

    # check for 'if' condition 1
    matched = phantom.decision(
        container=container,
        action_results=results,
        conditions=[
            ["run_Email_Hash_query:action_result.summary.total_events", ">", 0],
        ])

    # call connected blocks if condition 1 matched
    if matched:
        Format_Email_Hash_Results(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)
        return

    # call connected blocks for 'else' condition 2
    Format_No_Email_Results(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)

    return

def Format_No_Email_Results(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('Format_No_Email_Results() called')
    
    template = """No Matching {2} Email Hash Found in Splunk between  _time={0} and _indextime={1}"""

    # parameter list for template variable replacement
    parameters = [
        "calculate_day_earliest_time:custom_function:earliest",
        "artifact:*.cef._indextime",
    ]

    phantom.format(container=container, template=template, parameters=parameters, name="Format_No_Email_Results")

    join_Format_Final_Hash_Results(container=container)

    return

def Check_Number_of_URL_results(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('Check_Number_of_URL_results() called')

    # check for 'if' condition 1
    matched = phantom.decision(
        container=container,
        action_results=results,
        conditions=[
            ["run_EMAIL_query:action_result.summary.total_events", ">", 0],
        ])

    # call connected blocks if condition 1 matched
    if matched:
        Format_Email_URL_Results(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)
        return

    # call connected blocks for 'else' condition 2
    Format_No_Email_URL_Results(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)

    return

def Format_Email_URL_Results(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('Format_Email_URL_Results() called')
    
    template = """Email URL Found in Splunk between  _time {0} and _indextime {1} 

%%
_time     {2}
src       {3}
dest    {4}
sourcetype  {5}
file_hash  {6}
url  {7}
Count {8}
%%"""

    # parameter list for template variable replacement
    parameters = [
        "calculate_day_earliest_time:custom_function:earliest",
        "artifact:*.cef._indextime",
        "run_EMAIL_query:action_result.data.*._time",
        "run_EMAIL_query:action_result.data.*.src",
        "run_EMAIL_query:action_result.data.*.dest",
        "run_EMAIL_query:action_result.data.*.sourcetype",
        "run_EMAIL_query:action_result.data.*.file_hash",
        "run_EMAIL_query:action_result.data.*.url",
        "run_EMAIL_query:action_result.data.*.Count",
    ]

    phantom.format(container=container, template=template, parameters=parameters, name="Format_Email_URL_Results")

    join_search_WEB_for_url_format(container=container)

    return

def Format_No_Email_URL_Results(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('Format_No_Email_URL_Results() called')
    
    template = """Format No Matching {2} Email URL Found in Splunk between  _time={0} and _indextime={1}"""

    # parameter list for template variable replacement
    parameters = [
        "calculate_day_earliest_time:custom_function:earliest",
        "artifact:*.cef._indextime",
        "artifact:*.cef.threat_match_value",
    ]

    phantom.format(container=container, template=template, parameters=parameters, name="Format_No_Email_URL_Results")

    join_search_WEB_for_url_format(container=container)

    return

def Check_Number_of_IP_Sessions_Results(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('Check_Number_of_IP_Sessions_Results() called')

    # check for 'if' condition 1
    matched = phantom.decision(
        container=container,
        action_results=results,
        conditions=[
            ["run_Network_Sessions_Query:action_result.summary.total_events", ">", 0],
        ])

    # call connected blocks if condition 1 matched
    if matched:
        Format_Network_Sessions_Results(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)
        return

    # call connected blocks for 'else' condition 2
    Format_No_Network_Session_Results(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)

    return

def Format_Final_Hash_Results(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('Format_Final_Hash_Results() called')
    
    template = """----------------------------------
File Hash Results
{0}{1}
----------------------------------
Email Hash Results
{2}{3}"""

    # parameter list for template variable replacement
    parameters = [
        "Format_FileHash_events:formatted_data",
        "Format_No_Email_Results:formatted_data",
        "Format_FileHash_events:formatted_data",
        "Format_No_Email_Results:formatted_data",
    ]

    phantom.format(container=container, template=template, parameters=parameters, name="Format_Final_Hash_Results")

    add_Hash_Notes(container=container)

    return

def join_Format_Final_Hash_Results(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None):
    phantom.debug('join_Format_Final_Hash_Results() called')

    # check if all connected incoming playbooks, actions, or custom functions are done i.e. have succeeded or failed
    if phantom.completed(action_names=['run_Email_Hash_query']):
        
        # call connected block "Format_Final_Hash_Results"
        Format_Final_Hash_Results(container=container, handle=handle)
    
    return

def decision_6(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('decision_6() called')

    # check for 'if' condition 1
    matched = phantom.decision(
        container=container,
        action_results=results,
        conditions=[
            ["run_Web_query:action_result.summary.total_events", ">", 0],
        ])

    # call connected blocks if condition 1 matched
    if matched:
        Format_WebURL_results(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)
        return

    # call connected blocks for 'else' condition 2
    Format_No_Web_Url_Results(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)

    return

def Format_No_Web_Url_Results(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('Format_No_Web_Url_Results() called')
    
    template = """No Matching {2} Web URL Found in Splunk between  _time={0} and _indextime={1}"""

    # parameter list for template variable replacement
    parameters = [
        "calculate_day_earliest_time:custom_function:earliest",
        "artifact:*.cef._indextime",
        "artifact:*.cef.threat_match_value",
    ]

    phantom.format(container=container, template=template, parameters=parameters, name="Format_No_Web_Url_Results")

    join_Format_Final_URL_Results(container=container)

    return

def Format_Final_URL_Results(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('Format_Final_URL_Results() called')
    
    template = """----------------------
Web URL Results
{0}{1}
----------------------
Email URL Results
{2}{3}"""

    # parameter list for template variable replacement
    parameters = [
        "Format_WebURL_results:formatted_data",
        "Format_No_Web_Url_Results:formatted_data",
        "Format_Email_URL_Results:formatted_data",
        "Format_No_Email_URL_Results:formatted_data",
    ]

    phantom.format(container=container, template=template, parameters=parameters, name="Format_Final_URL_Results")

    add_URL_Notes(container=container)

    return

def join_Format_Final_URL_Results(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None):
    phantom.debug('join_Format_Final_URL_Results() called')

    # check if all connected incoming playbooks, actions, or custom functions are done i.e. have succeeded or failed
    if phantom.completed(action_names=['run_Web_query']):
        
        # call connected block "Format_Final_URL_Results"
        Format_Final_URL_Results(container=container, handle=handle)
    
    return

def Format_Network_Sessions_Results(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('Format_Network_Sessions_Results() called')
    
    template = """Network Sessions  for {2} Found in Splunk between  _time {0} and _indextime {1} 

%%
_time {3}
sourcetype {4}
app {5}
action {6}
dest_ip {7}
src_ip {8}
user {9}
%%
Count
%%"""

    # parameter list for template variable replacement
    parameters = [
        "calculate_day_earliest_time:custom_function:earliest",
        "filtered-data:filter_url_or_ip_or_hash:condition_2:artifact:*.cef._indextime",
        "filtered-data:filter_url_or_ip_or_hash:condition_2:artifact:*.cef.threat_match_value",
        "run_Network_Sessions_Query:action_result.data.*._time",
        "run_Network_Sessions_Query:action_result.data.*.sourcetype",
        "run_Network_Sessions_Query:action_result.data.*.app",
        "run_Network_Sessions_Query:action_result.data.*.action",
        "run_Network_Sessions_Query:action_result.data.*.dest_ip",
        "run_Network_Sessions_Query:action_result.data.*.src_ip",
        "run_Network_Sessions_Query:action_result.data.*.user",
    ]

    phantom.format(container=container, template=template, parameters=parameters, name="Format_Network_Sessions_Results")

    join_search_Network_Traffic_format(container=container)

    return

def Format_No_Network_Session_Results(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('Format_No_Network_Session_Results() called')
    
    template = """Format No Matching {2} Network Session Found in Splunk between  _time={0} and _indextime={1}"""

    # parameter list for template variable replacement
    parameters = [
        "calculate_day_earliest_time:custom_function:earliest",
        "artifact:*.cef._indextime",
        "artifact:*.cef.threat_match_value",
    ]

    phantom.format(container=container, template=template, parameters=parameters, name="Format_No_Network_Session_Results")

    join_search_Network_Traffic_format(container=container)

    return

def Format_No_Network_Traffic_Results(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('Format_No_Network_Traffic_Results() called')
    
    template = """No Matching {2}Web URL Found in Splunk between  _time={0} and _indextime={1}"""

    # parameter list for template variable replacement
    parameters = [
        "calculate_day_earliest_time:custom_function:earliest",
        "filtered-data:filter_url_or_ip_or_hash:condition_2:artifact:*.cef._indextime",
        "artifact:*.cef.threat_match_field",
    ]

    phantom.format(container=container, template=template, parameters=parameters, name="Format_No_Network_Traffic_Results")

    join_Format_Final_IP_Results(container=container)

    return

def Check_for_Network_Traffic_Results(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('Check_for_Network_Traffic_Results() called')

    # check for 'if' condition 1
    matched = phantom.decision(
        container=container,
        action_results=results,
        conditions=[
            ["run_Network_Traffic_query:action_result.summary.total_events", ">", 0],
        ])

    # call connected blocks if condition 1 matched
    if matched:
        Format_Network_Results(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)
        return

    # call connected blocks for 'else' condition 2
    Format_No_Network_Traffic_Results(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)

    return

def Format_Final_IP_Results(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('Format_Final_IP_Results() called')
    
    template = """----------------------
Network Sessions Results
{0}{1}
----------------------
Network Traffic Results
{2}{3}"""

    # parameter list for template variable replacement
    parameters = [
        "Format_Network_Sessions_Results:formatted_data",
        "Format_No_Network_Session_Results:formatted_data",
        "Format_Network_Results:formatted_data",
        "Format_No_Network_Traffic_Results:formatted_data",
    ]

    phantom.format(container=container, template=template, parameters=parameters, name="Format_Final_IP_Results")

    add_IP_Notes(container=container)

    return

def join_Format_Final_IP_Results(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None):
    phantom.debug('join_Format_Final_IP_Results() called')

    # check if all connected incoming playbooks, actions, or custom functions are done i.e. have succeeded or failed
    if phantom.completed(action_names=['run_Network_Traffic_query']):
        
        # call connected block "Format_Final_IP_Results"
        Format_Final_IP_Results(container=container, handle=handle)
    
    return

def add_URL_Notes(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('add_URL_Notes() called')

    formatted_data_1 = phantom.get_format_data(name='Format_Final_URL_Results')
    
    task_data = {}
    task_name = "Determine additional compromised systems"
    note_type = "general"
    task_id = ""
    
    # Get the tasks for start of the workbook
    for task in phantom.get_tasks(container=container):
        # Get the right task
        if task['data']['name'] == task_name:
            task_data.update(task['data'])
            phantom.debug('phantom.get_tasks found the task: task_id: {}, task_name: {}'.format(task_data['id'],task_data['name']))
            note_type = "task"
            task_id = task_data['id']
        else: 
            phantom.debug('phantom.get_tasks did NOT found the task_name: {}'.format(task_name))
            
    note_title = "Possible compromised Host(s) from URL or Domain"
    note_content = formatted_data_1
    note_format = "markdown"
    phantom.add_note(container=container, note_type=note_type, task_id=task_id, title=note_title, content=note_content, note_format=note_format)

    return

def add_IP_Notes(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('add_IP_Notes() called')

    formatted_data_1 = phantom.get_format_data(name='Format_Final_IP_Results')
        
    task_data = {}
    task_name = "Determine additional compromised systems"
    note_type = "general"
    task_id = ""
    
    # Get the task for the note
    for task in phantom.get_tasks(container=container):
        # Get the right task
        if task['data']['name'] == task_name:
            task_data.update(task['data'])
            phantom.debug('phantom.get_tasks found the task: task_id: {}, task_name: {}'.format(task_data['id'],task_data['name']))
            note_type = "task"
            task_id = task_data['id']
        else: 
            phantom.debug('phantom.get_tasks did NOT found the task_name: {}'.format(task_name))

    note_title = "Possible compromised Host(s) from IP"
    note_content = formatted_data_1
    note_format = "markdown"
    phantom.add_note(container=container, note_type=note_type, task_id=task_id, title=note_title, content=note_content, note_format=note_format)

    return

"""
Added Task lookup for task id and note type:

note_task = "general"
    task_id = ""
    
    # Get the tasks for start of the workbook
    for task in phantom.get_tasks(container=container):
        ## gets the current phase and 1st task
        if task['data']['name'] == "Determine additional compromised systems" :
            task_data.update(task['data'])
            phantom.debug('phantom.get_tasks found the task: task_id: {}, task_name: {}'.format(task_data['id'],task_data['name']))
            note_type = "task"
            task_id = task_data['id']
"""
def add_Hash_Notes(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('add_Hash_Notes() called')

    formatted_data_1 = phantom.get_format_data(name='Format_Final_Hash_Results')
    
    task_data = {}
    task_name = "Determine additional compromised systems"
    note_type = "general"
    task_id = ""
    
    # Get the tasks for start of the workbook
    for task in phantom.get_tasks(container=container):
        # Get the right task
        if task['data']['name'] == task_name:
            task_data.update(task['data'])
            phantom.debug('phantom.get_tasks found the task: task_id: {}, task_name: {}'.format(task_data['id'],task_data['name']))
            note_type = "task"
            task_id = task_data['id']
        else: 
            phantom.debug('phantom.get_tasks did NOT found the task_name: {}'.format(task_name))
    
    note_title = "Possible compromised Host(s) from Hash"
    note_content = formatted_data_1
    note_format = "markdown"
    phantom.add_note(container=container, note_type=note_type, task_id=task_id, title=note_title, content=note_content, note_format=note_format)

    return

def missing_artifacts(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('missing_artifacts() called')

    phantom.comment(container=container, comment="Hunt Compromised playbook did not find any artifacts to process")

    return

def filter_artifact_severity(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('filter_artifact_severity() called')

    # collect filtered artifact ids for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        action_results=results,
        conditions=[
            ["artifact:*.severity", "==", "high"],
            ["artifact:*.severity", "==", "critical"],
            ["APT", "==", "artifact:*.tags"],
            ["malware", "==", "artifact:*.tags"],
            ["suspicious", "==", "artifact:*.tags"],
        ],
        logical_operator='or',
        name="filter_artifact_severity:condition_1")

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        filter_url_or_ip_or_hash(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

    return

def merge_hashes(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('merge_hashes() called')
    
    parameters = []

    parameters.append({
        'input_1': None,
        'input_2': None,
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

    # call custom function "community/list_merge", returns the custom_function_run_id
    phantom.custom_function(custom_function='community/list_merge', parameters=parameters, name='merge_hashes', callback=search_File_Hash_format)

    return

def merge_domains_urls(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('merge_domains_urls() called')
    
    filtered_artifacts_data_0 = phantom.collect2(container=container, datapath=['filtered-data:filter_url_or_ip_or_hash:condition_1:artifact:*.cef.requestURL', 'filtered-data:filter_url_or_ip_or_hash:condition_1:artifact:*.cef.url', 'filtered-data:filter_url_or_ip_or_hash:condition_1:artifact:*.cef.destinationDnsDomain', 'filtered-data:filter_url_or_ip_or_hash:condition_1:artifact:*.cef.dntdom', 'filtered-data:filter_url_or_ip_or_hash:condition_1:artifact:*.cef.sourceDnsDomain', 'filtered-data:filter_url_or_ip_or_hash:condition_1:artifact:*.cef.sntdom'])

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

    # call custom function "community/list_merge", returns the custom_function_run_id
    phantom.custom_function(custom_function='community/list_merge', parameters=parameters, name='merge_domains_urls', callback=search_Email_url_format)

    return

def merge_ips(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('merge_ips() called')
    
    filtered_artifacts_data_0 = phantom.collect2(container=container, datapath=['filtered-data:filter_url_or_ip_or_hash:condition_2:artifact:*.cef.destinationAddress', 'filtered-data:filter_url_or_ip_or_hash:condition_2:artifact:*.cef.dest', 'filtered-data:filter_url_or_ip_or_hash:condition_2:artifact:*.cef.dest_ip', 'filtered-data:filter_url_or_ip_or_hash:condition_2:artifact:*.cef.sourceAddress', 'filtered-data:filter_url_or_ip_or_hash:condition_2:artifact:*.cef.src', 'filtered-data:filter_url_or_ip_or_hash:condition_2:artifact:*.cef.src_ip'])

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

    # call custom function "community/list_merge", returns the custom_function_run_id
    phantom.custom_function(custom_function='community/list_merge', parameters=parameters, name='merge_ips', callback=search_Network_Sessions_Format)

    return

"""
Need to customize to get the playbook user and set the prompt for them. 

username  = phantom.collect2(container=container, datapath=['get_phantom_username:action_result.data.*.response_body.data.*.username'], action_results=results)

user = username
"""
def get_days_to_hunt_for(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('get_days_to_hunt_for() called')
    
    # get username from previous action run and present here for the user parameter
    username  = phantom.collect2(container=container, datapath=['get_phantom_username:action_result.data.*.response_body.username'], action_results=results)
    #phantom.debug(username)
    
    # set user and message variables for phantom.prompt call
    user = username[0][0]
    message = """This playbook will create a recursive search for a maximum of 90 days.  It will used any artifact with the tags \"APT\", \"malware\", \"suspicious\" or the following severities \"Critical\", or \"High\".  Mediums will need a tag to be searched. 

Please select the number of days to search.
We recommend no more than 90 days!!"""

    #responses:
    response_types = [
        {
            "prompt": "Please select the number of days to search. We recommend no more than 90 days!!",
            "options": {
                "type": "range",
                "min": 1,
                "max": 90,
            },
        },
    ]

    phantom.prompt2(container=container, user=user, message=message, respond_in_mins=30, name="get_days_to_hunt_for", response_types=response_types, callback=calculate_day_earliest_time)

    return

def in_process_task(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('in_process_task() called')
    
    results_data_1 = phantom.collect2(container=container, datapath=['get_workbook_task:action_result.data.*.response_body.data'], action_results=results)
    results_item_1_0 = [item[0] for item in results_data_1]

    in_process_task__task_body = None
    in_process_task__task_id = None
    in_process_task__owner = None

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Gets playbook info to get current running user
    in_process_task__owner = 0
    pb_info = phantom.get_playbook_info()
    phantom.debug("Retreving owner name: {0}".format(pb_info[0]["effective_user_id"]))
    in_process_task__owner = pb_info[0]["effective_user_id"]
    
    # Get tasks and update task body
    task_data = []
    in_process_task__task_body = []

    # Add found task data to process
    #phantom.debug(results_data_1)
    if results_data_1[0][0]:
        task_data = results_data_1[0][0][0]

    # Assign new attributes to task body
    if task_data:
        # Set owner
        in_process_task__task_body = {
            "owner": in_process_task__owner,
            "is_note_required": False,
            "status" : 2
        }         
        in_process_task__task_id = task_data["id"]
        in_process_task__note_data = task_data["notes"]
        in_process_task__task_name = task_data["name"]
        phantom.debug("We are updating Task Id: {} named {}".format(in_process_task__task_id,in_process_task__task_name))
    else:
        phantom.debug("There was no task was presented to the block. We will create a standalone hunt")

    #phantom.debug(in_process_task__task_body)
    #phantom.debug(in_process_task__note_data)

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key='in_process_task:task_body', value=json.dumps(in_process_task__task_body))
    phantom.save_run_data(key='in_process_task:task_id', value=json.dumps(in_process_task__task_id))
    phantom.save_run_data(key='in_process_task:owner', value=json.dumps(in_process_task__owner))
    Check_for_threat_match_field(container=container)

    return

"""
Need to modify for different task names if they change. This one is set to "Determine additional compromised systems"
"""
def workbook_task_url(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('workbook_task_url() called')
    
    template = """/workbook_task/?_filter_container={0}&_filter_name__startswith=\"Determine additional compromised systems\"&_filter_status__in=[0,2]&sort=order&order=asc&page_size=1"""

    # parameter list for template variable replacement
    parameters = [
        "container:id",
    ]

    phantom.format(container=container, template=template, parameters=parameters, name="workbook_task_url")

    get_workbook_task(container=container)

    return

def get_workbook_task(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('get_workbook_task() called')

    # collect data for 'get_workbook_task' call
    formatted_data_1 = phantom.get_format_data(name='workbook_task_url')

    parameters = []
    
    # build parameters list for 'get_workbook_task' call
    parameters.append({
        'headers': "",
        'location': formatted_data_1,
        'verify_certificate': False,
    })

    phantom.act(action="get data", parameters=parameters, assets=['phantom_rest_api'], callback=in_process_task, name="get_workbook_task")

    return

def task_url_format(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('task_url_format() called')
    
    template = """/workflow_task/{0}"""

    # parameter list for template variable replacement
    parameters = [
        "in_process_task:custom_function:task_id",
    ]

    phantom.format(container=container, template=template, parameters=parameters, name="task_url_format")

    update_task_to_in_process(container=container)

    return

def standalone_hunt(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('standalone_hunt() called')

    phantom.comment(container=container, comment="No available workbook task. Running hunt as stand alone")
    join_user_url_format(container=container)

    return

def update_task_to_in_process(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('update_task_to_in_process() called')
        
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    in_process_task__task_body = json.loads(phantom.get_run_data(key='in_process_task:task_body'))
    # collect data for 'update_task_to_in_process' call
    formatted_data_1 = phantom.get_format_data(name='task_url_format')

    parameters = []
    
    # build parameters list for 'update_task_to_in_process' call
    parameters.append({
        'body': in_process_task__task_body,
        'headers': "",
        'location': formatted_data_1,
        'verify_certificate': "",
    })

    phantom.act(action="post data", parameters=parameters, assets=['phantom_rest_api'], callback=join_user_url_format, name="update_task_to_in_process")

    return

def user_url_format(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('user_url_format() called')
    
    template = """ph_user/{0}"""

    # parameter list for template variable replacement
    parameters = [
        "in_process_task:custom_function:owner",
    ]

    phantom.format(container=container, template=template, parameters=parameters, name="user_url_format")

    get_phantom_username(container=container)

    return

def join_user_url_format(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None):
    phantom.debug('join_user_url_format() called')
    
    # if the joined function has already been called, do nothing
    if phantom.get_run_data(key='join_user_url_format_called'):
        return

    # no callbacks to check, call connected block "user_url_format"
    phantom.save_run_data(key='join_user_url_format_called', value='user_url_format', auto=True)

    user_url_format(container=container, handle=handle)
    
    return

def get_phantom_username(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('get_phantom_username() called')
        
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'get_phantom_username' call
    formatted_data_1 = phantom.get_format_data(name='user_url_format')

    parameters = []
    
    # build parameters list for 'get_phantom_username' call
    parameters.append({
        'headers': "",
        'location': formatted_data_1,
        'verify_certificate': False,
    })

    phantom.act(action="get data", parameters=parameters, assets=['phantom_rest_api'], callback=get_days_to_hunt_for, name="get_phantom_username")

    return

def decision_8(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('decision_8() called')

    # check for 'if' condition 1
    matched = phantom.decision(
        container=container,
        action_results=results,
        conditions=[
            ["get_days_to_hunt_for:action_result.status", "==", "success"],
        ])

    # call connected blocks if condition 1 matched
    if matched:
        calculate_day_earliest_time(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)
        return

    # call connected blocks for 'else' condition 2
    failed_prompt_comment(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)

    return

def failed_prompt_comment(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('failed_prompt_comment() called')

    phantom.comment(container=container, comment="Prompt SLA expired or Prompt failure.  Please check Activity and if necessary debug or rerun playbook to start again.")

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