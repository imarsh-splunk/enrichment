"""
This playbook take usernames and hostnames and conducts Splunk searches on them and prints out a note on what it finds from Splunk.
"""

import phantom.rules as phantom
import json
from datetime import datetime, timedelta
def on_start(container):
    phantom.debug('on_start() called')
    
    # call 'check_user_and_host' block
    check_user_and_host(container=container)

    return

"""
Check for user and ip parameters not in bogon_list
"""
def check_user_and_host(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('check_user_and_host() called')

    # check for 'if' condition 1
    matched = phantom.decision(
        container=container,
        conditions=[
            ["artifact:*.cef.destinationUserId", "not in", "custom_list:bogon_list"],
            ["artifact:*.cef.destinationUserName", "not in", "custom_list:bogon_list"],
            ["artifact:*.cef.duser", "not in", "custom_list:bogon_list"],
            ["artifact:*.cef.sourceUserId", "not in", "custom_list:bogon_list"],
            ["artifact:*.cef.sourceUserName", "not in", "custom_list:bogon_list"],
            ["artifact:*.cef.suser", "not in", "custom_list:bogon_list"],
            ["artifact:*.cef.dest", "in", "custom_list:bogon_list"],
            ["artifact:*.cef.destinationAddress", "in", "custom_list:bogon_list"],
            ["artifact:*.cef.dest_ip", "in", "custom_list:bogon_list"],
            ["artifact:*.cef.destinationHostName", "not in", "custom_list:bogon_list"],
            ["artifact:*.cef.src", "in", "custom_list:bogon_list"],
            ["artifact:*.cef.src_ip", "in", "custom_list:bogon_list"],
            ["artifact:*.cef.sourceAddress", "in", "custom_list:bogon_list"],
            ["artifact:*.cef.sourceHostName", "not in", "custom_list:bogon_list"],
            ["artifact:*.cef.dhost", "not in", "custom_list:bogon_list"],
            ["artifact:*.cef.shost", "not in", "custom_list:bogon_list"],
        ],
        logical_operator='or')

    # call connected blocks if condition 1 matched
    if matched:
        user_and_host_filter(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)
        return

    # call connected blocks for 'else' condition 2
    missing_data_comment(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)

    return

def missing_data_comment(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('missing_data_comment() called')

    phantom.comment(container=container, comment="Missing user or host information to execute playbook.")

    return

def user_and_host_filter(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('user_and_host_filter() called')

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
        name="user_and_host_filter:condition_1")

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        merge_usernames(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

    # collect filtered artifact ids for 'if' condition 2
    matched_artifacts_2, matched_results_2 = phantom.condition(
        container=container,
        conditions=[
            ["artifact:*.cef.dest", "in", "custom_list:bogon_list"],
            ["artifact:*.cef.destinationAddress", "not in", "custom_list:bogon_list"],
            ["artifact:*.cef.dest_ip", "==", "custom_list:bogon_list"],
            ["artifact:*.cef.destinationHostName", "in", "custom_list:bogon_list"],
            ["artifact:*.cef.src", "in", "custom_list:bogon_list"],
            ["artifact:*.cef.src_ip", "in", "custom_list:bogon_list"],
            ["artifact:*.cef.sourceAddress", "in", "custom_list:bogon_list"],
            ["artifact:*.cef.dhost", "not in", "custom_list:bogon_list"],
            ["artifact:*.cef.shost", "not in", "custom_list:bogon_list"],
            ["artifact:*.cef.sourceHostName", "not in", "custom_list:bogon_list"],
        ],
        logical_operator='or',
        name="user_and_host_filter:condition_2")

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_2 or matched_results_2:
        merge_hostnames(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function, filtered_artifacts=matched_artifacts_2, filtered_results=matched_results_2)

    return

def create_user_task_url(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('create_user_task_url() called')
    
    template = """/workbook_task/{0}"""

    # parameter list for template variable replacement
    parameters = [
        "create_user_notes:custom_function:task_id",
    ]

    phantom.format(container=container, template=template, parameters=parameters, name="create_user_task_url")

    create_user_task_note(container=container)

    return

"""
earliest="-7d"
"""
def format_user_spl_query(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('format_user_spl_query() called')
    
    template = """%%
| tstats latest(_time) as last_login_time , count as login_count from datamodel=Authentication WHERE (index=*  Authentication.src_user !=*$  Authentication.user !=*$ Authentication.action = success  Authentication.user = \"*{0}*\" )  by  Authentication.user Authentication.dest  | rename Authentication.user as user, Authentication.dest as computer | convert ctime(last_login_time)  | table computer user login_count last_login_time
%%"""

    # parameter list for template variable replacement
    parameters = [
        "merge_usernames:custom_function_result.data.*.item",
    ]

    phantom.format(container=container, template=template, parameters=parameters, name="format_user_spl_query")

    run_user_spl_query(container=container)

    return

def run_user_spl_query(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('run_user_spl_query() called')
        
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'run_user_spl_query' call
    formatted_data_1 = phantom.get_format_data(name='format_user_spl_query__as_list')

    parameters = []
    
    # build parameters list for 'run_user_spl_query' call
    for formatted_part_1 in formatted_data_1:
        parameters.append({
            'query': formatted_part_1,
            'command': "",
            'display': "Computer,user,login_count,last_login_time",
            'parse_only': "",
        })

    phantom.act(action="run query", parameters=parameters, assets=['splunk-es-kelby'], callback=format_user_spl_results, name="run_user_spl_query")

    return

def create_user_notes(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('create_user_notes() called')
    
    input_parameter_0 = "Validate customer and endpoint Information"
    input_parameter_1 = "User Analysis Notes:"
    formatted_data_1 = phantom.get_format_data(name='format_user_spl_results')

    create_user_notes__note_params = None
    create_user_notes__task_id = None

    ################################################################################
    ## Custom Code Start
    ################################################################################

    task_data = {}
    note_params = []
    
    # print debug statement
    #phantom.debug(formatted_data_1)
    
    if formatted_data_1:
        content = formatted_data_1
    else:
        content = """ There was a failure in the action"""
    
    for task in phantom.get_tasks(container=container):
        ## gets the current phase and  get 3rd tash(Review Indicators)
        if task['data']['name'] == input_parameter_0:
            task_data.update(task['data'])
            phantom.debug('phantom.get_tasks found Task "{}" with the task_id: {}, task_name: {}'.format(input_parameter_0,task_data['id'],task_data['name']))
        
    note_params.append({
            "note_type": "task",
            "task_id": task_data['id'],
            "container_id": container['id'],
            "title": input_parameter_1,
            "content": content,
            "phase_id": task_data['phase'],
        })
    
    create_user_notes__note_params = note_params
    create_user_notes__task_id = task_data['id']

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key='create_user_notes:note_params', value=json.dumps(create_user_notes__note_params))
    phantom.save_run_data(key='create_user_notes:task_id', value=json.dumps(create_user_notes__task_id))
    create_user_task_url(container=container)

    return

"""
earliest="-7d"
"""
def format_host_spl_query(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('format_host_spl_query() called')
    
    template = """%%
| tstats latest(_time) as last_login_time , count as login_count from datamodel=Authentication WHERE (index=*  Authentication.src_user !=*$  Authentication.user !=*$ Authentication.action = success Authentication.dest=\"*{0}*\" )  by  Authentication.user Authentication.dest  | rename Authentication.user as user, Authentication.dest as computer | convert ctime(last_login_time) | head 10 | table computer user login_count last_login_time
%%"""

    # parameter list for template variable replacement
    parameters = [
        "merge_hostnames:custom_function_result.data.*.item",
    ]

    phantom.format(container=container, template=template, parameters=parameters, name="format_host_spl_query")

    run_host_spl_query(container=container)

    return

def run_host_spl_query(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('run_host_spl_query() called')
        
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'run_host_spl_query' call
    formatted_data_1 = phantom.get_format_data(name='format_host_spl_query__as_list')

    parameters = []
    
    # build parameters list for 'run_host_spl_query' call
    for formatted_part_1 in formatted_data_1:
        parameters.append({
            'query': formatted_part_1,
            'command': "",
            'display': "Computer,user,login_count,last_login_time",
            'parse_only': "",
        })

    phantom.act(action="run query", parameters=parameters, assets=['splunk-es-kelby'], callback=format_host_spl_results, name="run_host_spl_query")

    return

def create_host_notes(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('create_host_notes() called')
    
    input_parameter_0 = "Validate customer and endpoint Information"
    input_parameter_1 = "Enumerate Logged-in Users:"
    formatted_data_1 = phantom.get_format_data(name='format_host_spl_results')

    create_host_notes__note_params = None
    create_host_notes__task_id = None

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # print debug statement
    #phantom.debug(formatted_data_1)
    
    if formatted_data_1:
        content = formatted_data_1
    else:
        content = """ There was a failure in the action"""
    
    task_data = {}
    note_params = []
    
    for task in phantom.get_tasks(container=container):
        ## gets the current phase and  get 3rd tash(Review Indicators)
        if task['data']['name'] == input_parameter_0:
            task_data.update(task['data'])
            phantom.debug('phantom.get_tasks found Task "{}" with the task_id: {}, task_name: {}'.format(input_parameter_0,task_data['id'],task_data['name']))
    
    note_params.append({
            "note_type": "task",
            "task_id": task_data['id'],
            "container_id": container['id'],
            "title": input_parameter_1,
            "content": content,
            "phase_id": task_data['phase']
        })

    create_host_notes__task_id = task_data['id']
    create_host_notes__note_params = note_params

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key='create_host_notes:note_params', value=json.dumps(create_host_notes__note_params))
    phantom.save_run_data(key='create_host_notes:task_id', value=json.dumps(create_host_notes__task_id))
    create_host_task_url(container=container)

    return

def create_host_task_url(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('create_host_task_url() called')
    
    template = """/workbook_task/{0}"""

    # parameter list for template variable replacement
    parameters = [
        "create_host_notes:custom_function:task_id",
    ]

    phantom.format(container=container, template=template, parameters=parameters, name="create_host_task_url")

    create_host_task_notes(container=container)

    return

"""
custom code:

for note_data in create_automated_notes__note_params:
        parameters.append({
            'location': "/note/",
            'body': json.dumps(note_data),
            'headers': "",
            'verify_certificate': False,
        })

"""
def create_host_task_notes(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('create_host_task_notes() called')
        
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    create_host_notes__note_params = phantom.get_run_data(key='create_host_notes:note_params')
    # collect data for 'create_host_task_notes' call

    parameters = []
    
    # build parameters list for 'create_host_task_notes' call
    parameters.append({
        'body': create_host_notes__note_params,
        'headers': "",
        'location': "/note/",
        'verify_certificate': False,
    })

    phantom.act(action="post data", parameters=parameters, assets=['phantom_rest_api'], name="create_host_task_notes")

    return

def format_user_spl_results(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('format_user_spl_results() called')
    
    template = """### Account Search Results Table: 

Message: {1}

| Computer | User, | login_count | last_login_time |
| ---- | ---- | ---- | ---- |
%%
| {2} | {3} | {4} | {5} | 
%%

**SPL Query:**  `{0}`"""

    # parameter list for template variable replacement
    parameters = [
        "run_user_spl_query:action_result.parameter.query",
        "run_user_spl_query:action_result.message",
        "run_user_spl_query:action_result.data.*.computer",
        "run_user_spl_query:action_result.data.*.user",
        "run_user_spl_query:action_result.data.*.login_count",
        "run_user_spl_query:action_result.data.*.last_login_time",
    ]

    phantom.format(container=container, template=template, parameters=parameters, name="format_user_spl_results")

    create_user_notes(container=container)

    return

def format_host_spl_results(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('format_host_spl_results() called')
    
    template = """### Host Search Results:

Message: {1}

| Computer | user, | login_count | last_login_time |
| ---- | ---- | ---- | ---- |
%%
| {2} | {3} | {4} | {5} | 
%%

**SPL Query:**  `{0}`"""

    # parameter list for template variable replacement
    parameters = [
        "run_host_spl_query:action_result.parameter.query",
        "run_host_spl_query:action_result.message",
        "run_host_spl_query:action_result.data.*.computer",
        "run_host_spl_query:action_result.data.*.user",
        "run_host_spl_query:action_result.data.*.login_count",
        "run_host_spl_query:action_result.data.*.last_login_time",
    ]

    phantom.format(container=container, template=template, parameters=parameters, name="format_host_spl_results")

    create_host_notes(container=container)

    return

def merge_usernames(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('merge_usernames() called')
    
    filtered_artifacts_data_0 = phantom.collect2(container=container, datapath=['filtered-data:user_and_host_filter:condition_1:artifact:*.cef.destinationUserId', 'filtered-data:user_and_host_filter:condition_1:artifact:*.cef.destinationUserName', 'filtered-data:user_and_host_filter:condition_1:artifact:*.cef.duser', 'filtered-data:user_and_host_filter:condition_1:artifact:*.cef.sourceUserId', 'filtered-data:user_and_host_filter:condition_1:artifact:*.cef.sourceUserName', 'filtered-data:user_and_host_filter:condition_1:artifact:*.cef.suser'])

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
    phantom.custom_function(custom_function='escu/list_merge_dedup', parameters=parameters, name='merge_usernames', callback=format_user_spl_query)

    return

def merge_hostnames(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('merge_hostnames() called')
    
    filtered_artifacts_data_0 = phantom.collect2(container=container, datapath=['filtered-data:user_and_host_filter:condition_2:artifact:*.cef.dest', 'filtered-data:user_and_host_filter:condition_2:artifact:*.cef.dest_ip', 'filtered-data:user_and_host_filter:condition_2:artifact:*.cef.destinationAddress', 'filtered-data:user_and_host_filter:condition_2:artifact:*.cef.destinationHostName', 'filtered-data:user_and_host_filter:condition_2:artifact:*.cef.src', 'filtered-data:user_and_host_filter:condition_2:artifact:*.cef.src_ip', 'filtered-data:user_and_host_filter:condition_2:artifact:*.cef.sourceAddress', 'filtered-data:user_and_host_filter:condition_2:artifact:*.cef.sourceHostName', 'filtered-data:user_and_host_filter:condition_2:artifact:*.cef.dhost', 'filtered-data:user_and_host_filter:condition_2:artifact:*.cef.shost'])

    parameters = []

    filtered_artifacts_data_0_0 = [item[0] for item in filtered_artifacts_data_0]
    filtered_artifacts_data_0_1 = [item[1] for item in filtered_artifacts_data_0]
    filtered_artifacts_data_0_2 = [item[2] for item in filtered_artifacts_data_0]
    filtered_artifacts_data_0_3 = [item[3] for item in filtered_artifacts_data_0]
    filtered_artifacts_data_0_4 = [item[4] for item in filtered_artifacts_data_0]
    filtered_artifacts_data_0_5 = [item[5] for item in filtered_artifacts_data_0]
    filtered_artifacts_data_0_6 = [item[6] for item in filtered_artifacts_data_0]
    filtered_artifacts_data_0_7 = [item[7] for item in filtered_artifacts_data_0]
    filtered_artifacts_data_0_8 = [item[8] for item in filtered_artifacts_data_0]
    filtered_artifacts_data_0_9 = [item[9] for item in filtered_artifacts_data_0]

    parameters.append({
        'input_1': filtered_artifacts_data_0_0,
        'input_2': filtered_artifacts_data_0_1,
        'input_3': filtered_artifacts_data_0_2,
        'input_4': filtered_artifacts_data_0_3,
        'input_5': filtered_artifacts_data_0_4,
        'input_6': filtered_artifacts_data_0_5,
        'input_7': filtered_artifacts_data_0_6,
        'input_8': filtered_artifacts_data_0_7,
        'input_9': filtered_artifacts_data_0_8,
        'input_10': filtered_artifacts_data_0_9,
    })
    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################    

    # call custom function "escu/list_merge_dedup", returns the custom_function_run_id
    phantom.custom_function(custom_function='escu/list_merge_dedup', parameters=parameters, name='merge_hostnames', callback=format_host_spl_query)

    return

"""
Need make sure the data is json serializable for body content
"""
def create_user_task_note(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('create_user_task_note() called')
        
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    create_user_notes__note_params = phantom.get_run_data(key='create_user_notes:note_params')
    # collect data for 'create_user_task_note' call

    parameters = []
    
    # build parameters list for 'create_user_task_note' call
    parameters.append({
        'location': "/note/",
        'body': create_user_notes__note_params,
        'headers': "",
        'verify_certificate': False,
    })

    phantom.act(action="post data", parameters=parameters, assets=['phantom_rest_api'], name="create_user_task_note")

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