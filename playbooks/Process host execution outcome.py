"""
This playbook assigns the event with the current phase first task in the current phase, close the task as completed and run the next playbook in the next task.
"""

import phantom.rules as phantom
import json
from datetime import datetime, timedelta
def on_start(container):
    phantom.debug('on_start() called')
    
    # call 'get_and_set_owner' block
    get_and_set_owner(container=container)

    return

def get_and_set_owner(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('get_and_set_owner() called')
    
    input_parameter_0 = ""

    get_and_set_owner__owner = None

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Gets playbook info to get current running user
    pb_info = phantom.get_playbook_info()
    #phantom.debug("Retreving owner name: {0}".format(pb_info))
    #phantom.debug(pb_info)
    
    # Sets owner
    phantom.set_owner(container=container, user=pb_info[0]["effective_user_id"])
    get_and_set_owner__owner = pb_info[0]["effective_user_id"]

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key='get_and_set_owner:owner', value=json.dumps(get_and_set_owner__owner))
    configure_container(container=container)

    return

def configure_container(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('configure_container() called')

    phantom.set_status(container=container, status="Open")
    task_update(container=container)

    return

"""
use get_phase() and  get_task() phantom api calls to update response plan
"""
def task_update(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('task_update() called')
    
    input_parameter_0 = "Accept and assign event"
    get_and_set_owner__owner = json.loads(phantom.get_run_data(key='get_and_set_owner:owner'))

    task_update__task_body = None
    task_update__task_id = None
    task_update__next_playbook = None

    ################################################################################
    ## Custom Code Start
    ################################################################################
    
    # Get the current phase
    #success, message, phase_id, phase_name = phantom.get_phase()

    #phantom.debug('phantom.get_phase results: success: {}, message: {}, phase_id: {}, phase_name: {}'.format(success, message, phase_id, phase_name))

    # Define task body for updating task. 
    """ Task status [ 0 = Incomplete, 2 = In Progress, 1 = Complete]"""
    task_body = {
        "owner": get_and_set_owner__owner,
        "is_note_required" : False,
        "status" : 2
    }
    
    task_data = {}
    next_task = {}
    
    # Get the tasks for start of the workbook
    for task in phantom.get_tasks(container=container):
        ## gets the current phase and 1st task
        if task['data']['name'] == input_parameter_0:
            task_data.update(task['data'])
            phantom.debug('phantom.get_tasks found the first task: task_id: {}, task_name: {}'.format(task_data['id'],task_data['name']))
    #phantom.debug(task_data)
    
    # get the next task in the order
    for task in phantom.get_tasks(container=container):
        ## gets the next task in the order
        if task_data['phase'] == task['data']['phase'] and task['data']['order'] == (task_data['order'] +1):
            next_task.update(task['data'])
            phantom.debug('phantom.get_tasks found the next task: task_id: {}, task_name: {}'.format(next_task['id'],next_task['name']))

    # Assign new attributes to task body based on status
    """ Task status [ 0 = Incomplete, 2 = In Progress, 1 = Complete]"""
    if task_data['status'] == 0 or task_data['status'] == 2:
        # Set owner and status
        task_update__task_body = task_body
        task_update__task_id = task_data["id"]
        phantom.debug("finished finding the task body for id: {} and saving.".format(task_update__task_id))
        ## checks next task for playbook data to call
        try:
            task_update__next_playbook = "{}/{}".format(next_task['suggestions']['playbooks'][0]['scm'],next_task['suggestions']['playbooks'][0]['playbook'])
            phantom.debug("Found the following next playbook to launch: {}".format(task_update__next_playbook))
        except:
            phantom.debug('Next task data does not have playbook to call.')         
    else:
        phantom.error('Task data status is completed and will not be modified')
    
    """ Debug statements
    phantom.debug(task_update__task_body)
    phantom.debug(task_update__task_id)
    phantom.debug(task_update__next_playbook)"""

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key='task_update:task_body', value=json.dumps(task_update__task_body))
    phantom.save_run_data(key='task_update:task_id', value=json.dumps(task_update__task_id))
    phantom.save_run_data(key='task_update:next_playbook', value=json.dumps(task_update__next_playbook))
    task_url_format(container=container)

    return

def task_url_format(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('task_url_format() called')
    
    template = """/workflow_task/{0}"""

    # parameter list for template variable replacement
    parameters = [
        "task_update:custom_function:task_id",
    ]

    phantom.format(container=container, template=template, parameters=parameters, name="task_url_format")

    check_task_body(container=container)

    return

"""
removed the json.loads() to keep the data a string as the rest api needs from the custom function block

revised code: line 146
task_update__task_body = phantom.get_run_data(key='task_update:task_body')
"""
def update_task_to_inprocess(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('update_task_to_inprocess() called')

    task_update__task_body = phantom.get_run_data(key='task_update:task_body')
    # collect data for 'update_task_to_inprocess' call
    formatted_data_1 = phantom.get_format_data(name='task_url_format')

    parameters = []
    
    # build parameters list for 'update_task_to_inprocess' call
    parameters.append({
        'location': formatted_data_1,
        'body': task_update__task_body,
        'headers': "",
        'verify_certificate': False,
    })

    phantom.act(action="post data", parameters=parameters, assets=['phantom_rest_api'], callback=task_complete, name="update_task_to_inprocess")

    return

def task_complete(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('task_complete() called')
    
    task_update__task_body = json.loads(phantom.get_run_data(key='task_update:task_body'))

    task_complete__task_body = None

    ################################################################################
    ## Custom Code Start
    ################################################################################

    """ Task status [ 0 = Incomplete, 2 = In Progress, 1 = Complete]"""
    # Updates task body for task completed
    task_update__task_body['status'] = 1
    task_complete__task_body = task_update__task_body
    
    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key='task_complete:task_body', value=json.dumps(task_complete__task_body))
    update_task_to_complete(container=container)

    return

"""
removed the json.loads() to keep the data a string as the rest api needs from the custom function block
"""
def update_task_to_complete(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('update_task_to_complete() called')
        
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    task_complete__task_body = phantom.get_run_data(key='task_complete:task_body')
    # collect data for 'update_task_to_complete' call
    formatted_data_1 = phantom.get_format_data(name='task_url_format')

    parameters = []
    
    # build parameters list for 'update_task_to_complete' call
    parameters.append({
        'location': formatted_data_1,
        'body': task_complete__task_body,
        'headers': "",
        'verify_certificate': False,
    })

    phantom.act(action="post data", parameters=parameters, assets=['phantom_rest_api'], callback=call_next_playbook, name="update_task_to_complete")

    return

"""
use task update parameter next_playbook to automatically update the next playbook called.

Custom lines:  228-234

    task_update__next_playbook = json.loads(phantom.get_run_data(key='task_update:next_playbook'))
    
    if task_update__next_playbook:    
        # call playbook "local/Set Priority", returns the playbook_run_id
        playbook_run_id = phantom.playbook(task_update__next_playbook, container=container)
    else:
        phantom.error("No playbook was found in the next task, reverting to manual mode")
        phantom.comment(container=container, comment="No playbook was found in the next task, reverting to manual mode")
"""
def call_next_playbook(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('call_next_playbook() called')
    task_update__next_playbook = json.loads(phantom.get_run_data(key='task_update:next_playbook'))
    
    if task_update__next_playbook:    
        # call playbook "local/Set Priority", returns the playbook_run_id
        playbook_run_id = phantom.playbook(task_update__next_playbook, container=container)
    else:
        phantom.error("No playbook was found in the next task, reverting to manual mode")
        phantom.comment(container=container, comment="No playbook was found in the next task, reverting to manual mode")

    return

def check_task_body(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('check_task_body() called')

    # check for 'if' condition 1
    matched = phantom.decision(
        container=container,
        conditions=[
            ["task_update:custom_function:task_body", "==", ""],
        ])

    # call connected blocks if condition 1 matched
    if matched:
        completed_task(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)
        return

    # call connected blocks for 'else' condition 2
    update_task_to_inprocess(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)

    return

def completed_task(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('completed_task() called')

    phantom.comment(container=container, comment="The task is completed, please run the next playbook in the task manually.")

    return

def check_for_hostname(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('check_for_hostname() called')

    # check for 'if' condition 1
    matched = phantom.decision(
        container=container,
        action_results=results,
        conditions=[
            ["artifact:*.cef.destinationHostName", "!=", ""],
            ["artifact:*.cef.dhost", "!=", ""],
            ["artifact:*.cef.dest", "!=", ""],
        ],
        logical_operator='and')

    # call connected blocks if condition 1 matched
    if matched:
        hostname_filter(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)
        return

    # call connected blocks for 'else' condition 2
    missing_data_comment(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)

    return

def missing_data_comment(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('missing_data_comment() called')

    phantom.comment(container=container, comment="Missing indicator to process Determine Host Process Outcome playbook. Please review parameters and artifacts for correct data.")

    return

def hostname_filter(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('hostname_filter() called')

    # collect filtered artifact ids for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        action_results=results,
        conditions=[
            ["artifact:*.cef.destinationHostName", "!=", ""],
            ["artifact:*.cef.dhost", "!=", ""],
            ["artifact:*.cef.dest", "!=", ""],
        ],
        logical_operator='and',
        name="hostname_filter:condition_1")

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        merge_hostnames(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

    return

def merge_hostnames(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('merge_hostnames() called')
    
    filtered_artifacts_data_0 = phantom.collect2(container=container, datapath=['filtered-data:hostname_filter:condition_1:artifact:*.cef.destinationHostName', 'filtered-data:hostname_filter:condition_1:artifact:*.cef.dhost', 'filtered-data:hostname_filter:condition_1:artifact:*.cef.dest'])

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

    # call custom function "community/list_merge", returns the custom_function_run_id
    phantom.custom_function(custom_function='community/list_merge', parameters=parameters, name='merge_hostnames', callback=search_for_notables)

    return

def search_for_notables(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('search_for_notables() called')
    
    template = """%%
| search `notable` | search \"{0}\" | expandtoken
%%"""

    # parameter list for template variable replacement
    parameters = [
        "merge_hostnames:custom_function_result.data.*.item",
    ]

    phantom.format(container=container, template=template, parameters=parameters, name="search_for_notables")

    get_notables_for_hostname(container=container)

    return

"""
| search `notable` | search "ops-sys-006" | expandtoken
"""
def get_notables_for_hostname(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('get_notables_for_hostname() called')
        
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'get_notables_for_hostname' call
    formatted_data_1 = phantom.get_format_data(name='search_for_notables__as_list')

    parameters = []
    
    # build parameters list for 'get_notables_for_hostname' call
    for formatted_part_1 in formatted_data_1:
        parameters.append({
            'query': formatted_part_1,
            'command': "search",
            'display': "_time, rule_name, owner, priority, severity, status_description, event_id",
            'parse_only': True,
        })

    phantom.act(action="run query", parameters=parameters, assets=['splunk_es'], name="get_notables_for_hostname")

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