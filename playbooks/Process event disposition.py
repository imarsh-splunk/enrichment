"""
This playbook helps close the determine event disposition workbook task.  The main purpose of the task is decide the appropriate disposition of the event and then automate those tasks to event closure.
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
    
    input_parameter_0 = "Determine process disposition"
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
        'body': task_update__task_body,
        'headers': "",
        'location': formatted_data_1,
        'verify_certificate': False,
    })

    phantom.act(action="post data", parameters=parameters, assets=['phantom_rest_api'], callback=user_url_format, name="update_task_to_inprocess")

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

def determine_event_disposition(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('determine_event_disposition() called')

    # Gets the current username for the playbook to assign the prompt correctly
    user_info = phantom.collect2(container=container, datapath=['get_user_info:action_result.data.*.response_body.username'], action_results=results)
    #phantom.debug(user_info)
    user = user_info[0][0]
        
    message = """What is the final disposition of this event?

associate - We will merge this with an existing case in Phantom.
event - This event/case requires IT and/or Security actions to resolve
non-event - Additional actions are required, but this is not a security event
false-positive - This event/case triggered on an approved or accepted indicator."""

    #responses:
    response_types = [
        {
            "prompt": "Event Disposition",
            "options": {
                "type": "list",
                "choices": [
                    "associate",
                    "event",
                    "non-event",
                    "false-positive",
                ]
            },
        },
        {
            "prompt": "Did you update the remedy ticket with the appropriate disposition?",
            "options": {
                "type": "list",
                "choices": [
                    "Yes",
                    "No",
                ]
            },
        },
    ]

    phantom.prompt2(container=container, user=user, message=message, respond_in_mins=30, name="determine_event_disposition", response_types=response_types, callback=disposition_status)

    return

def user_url_format(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('user_url_format() called')
    
    template = """ph_user/{0}"""

    # parameter list for template variable replacement
    parameters = [
        "get_and_set_owner:custom_function:owner",
    ]

    phantom.format(container=container, template=template, parameters=parameters, name="user_url_format")

    get_user_info(container=container)

    return

def get_user_info(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('get_user_info() called')
        
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'get_user_info' call
    formatted_data_1 = phantom.get_format_data(name='user_url_format')

    parameters = []
    
    # build parameters list for 'get_user_info' call
    parameters.append({
        'headers': "",
        'location': formatted_data_1,
        'verify_certificate': False,
    })

    phantom.act(action="get data", parameters=parameters, assets=['phantom_rest_api'], callback=determine_event_disposition, name="get_user_info")

    return

def disposition_results(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('disposition_results() called')

    # check for 'if' condition 1
    matched = phantom.decision(
        container=container,
        action_results=results,
        conditions=[
            ["determine_event_disposition:action_result.summary.responses.0", "==", "associate"],
        ])

    # call connected blocks if condition 1 matched
    if matched:
        associate_events(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)
        return

    # call connected blocks for 'else' condition 2
    assign_workbook(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)

    return

def disposition_status(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('disposition_status() called')

    # check for 'if' condition 1
    matched = phantom.decision(
        container=container,
        action_results=results,
        conditions=[
            ["determine_event_disposition:action_result.status", "==", "success"],
        ])

    # call connected blocks if condition 1 matched
    if matched:
        disposition_tag(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)
        return

    return

def associate_events(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('associate_events() called')
    
    # call playbook "gitlab-Playbooks/associate and merge events into case", returns the playbook_run_id
    playbook_run_id = phantom.playbook(playbook="gitlab-Playbooks/associate and merge events into case", container=container)
    join_task_complete(container=container)

    return

def assign_workbook(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('assign_workbook() called')
    
    # call playbook "gitlab-Playbooks/Assign workbook and set current phase", returns the playbook_run_id
    playbook_run_id = phantom.playbook(playbook="gitlab-Playbooks/Assign workbook and set current phase", container=container)
    join_task_complete(container=container)

    return

"""
API doesn't allow variable tags, this enables that ability. Applies tag to event corresponding to its disposition. 

REPLACE:

phantom.comment(container=container, comment=results_item_1_0)

    phantom.add_tags(container=container, tags="placeholder")

WITH:

#phantom.comment(container=container, comment=results_item_1_0)

    phantom.add_tags(container=container, tags=results_item_1_0)
"""
def disposition_tag(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('disposition_tag() called')

    results_data_1 = phantom.collect2(container=container, datapath=['determine_event_disposition:action_result.summary.responses.0'], action_results=results)

    results_item_1_0 = [item[0] for item in results_data_1]

    #phantom.comment(container=container, comment=results_item_1_0)

    phantom.add_tags(container=container, tags=results_item_1_0)
    disposition_results(container=container)

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

def join_task_complete(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None):
    phantom.debug('join_task_complete() called')
    
    # if the joined function has already been called, do nothing
    if phantom.get_run_data(key='join_task_complete_called'):
        return

    # no callbacks to check, call connected block "task_complete"
    phantom.save_run_data(key='join_task_complete_called', value='task_complete', auto=True)

    task_complete(container=container, handle=handle)
    
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

    phantom.act(action="post data", parameters=parameters, assets=['phantom_rest_api'], name="update_task_to_complete")

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