"""
This utility playbook takes a tag to the container and assigns the workbook and current phase and removes the tag
"""

import phantom.rules as phantom
import json
from datetime import datetime, timedelta
def on_start(container):
    phantom.debug('on_start() called')
    
    # call 'container_url_format' block
    container_url_format(container=container)

    return

def missing_workbook_tag(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('missing_workbook_tag() called')

    phantom.comment(container=container, comment="No workbook tag found or failed to respond to prompt. Manually add workbook to event")

    return

def join_missing_workbook_tag(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None):
    phantom.debug('join_missing_workbook_tag() called')

    # check if all connected incoming playbooks, actions, or custom functions are done i.e. have succeeded or failed
    if phantom.completed(action_names=['Assign_workbook']):
        
        # call connected block "missing_workbook_tag"
        missing_workbook_tag(container=container, handle=handle)
    
    return

def container_url_format(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('container_url_format() called')
    
    template = """/container/{0}"""

    # parameter list for template variable replacement
    parameters = [
        "container:id",
    ]

    phantom.format(container=container, template=template, parameters=parameters, name="container_url_format")

    container_phases_format(container=container)

    return

def container_phases_format(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('container_phases_format() called')
    
    template = """/container/{0}/phases"""

    # parameter list for template variable replacement
    parameters = [
        "container:id",
    ]

    phantom.format(container=container, template=template, parameters=parameters, name="container_phases_format")

    get_workbook_templates(container=container)

    return

def user_url_format(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('user_url_format() called')
    
    template = """ph_user/{0}"""

    # parameter list for template variable replacement
    parameters = [
        "prompt_format:custom_function:user_id",
    ]

    phantom.format(container=container, template=template, parameters=parameters, name="user_url_format")

    get_user_name(container=container)

    return

def get_workbook_templates(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('get_workbook_templates() called')

    # collect data for 'get_workbook_templates' call

    parameters = []
    
    # build parameters list for 'get_workbook_templates' call
    parameters.append({
        'headers': "",
        'location': "/workbook_template",
        'verify_certificate': False,
    })

    phantom.act(action="get data", parameters=parameters, assets=['phantom_rest_api'], callback=prompt_format, name="get_workbook_templates")

    return

"""
Custom code modification on lines 214-224
    # Get required prompt data
    username = phantom.collect2(container=container, datapath=['get_user_name:action_result.data.*.response_body.username'], action_results=results)[0][0]
    phantom.debug("The effective playbook username is: {}".format(username))
    templates = phantom.collect2(container=container, datapath=['get_workbook_templates:action_result.data.*.response_body.data.*.name'], action_results=results)
    workbooks = [item[0] for item in templates]
    #phantom.debug(workbooks)
    
    # set user and message variables for phantom.prompt call
    user = username
"""
def Assign_workbook(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('Assign_workbook() called')
    
    # Get required prompt data
    username = phantom.collect2(container=container, datapath=['get_user_name:action_result.data.*.response_body.username'], action_results=results)[0][0]
    phantom.debug("The effective playbook username is: {}".format(username))
    templates = phantom.collect2(container=container, datapath=['get_workbook_templates:action_result.data.*.response_body.data.*.name'], action_results=results)
    workbooks = [item[0] for item in templates]
    workbooks.insert(0,"None")
    #phantom.debug(workbooks)
    
    # set user and message variables for phantom.prompt call
    user = username
    message = """{1},

Please respond to the questions below for event: {0}"""

    # parameter list for template variable replacement
    parameters = [
        "container:name",
        "get_user_name:action_result.data.*.response_body.username",
    ]

    #responses:
    response_types = [
        {
            "prompt": "Do you need to create a case?",
            "options": {
                "type": "list",
                "choices": [
                    "Yes",
                    "No",
                ]
            },
        },
        {
            "prompt": "Please select the workbook to assign:",
            "options": {
                "type": "list",
                "choices": workbooks
            },
        },
    ]

    phantom.prompt2(container=container, user=user, message=message, respond_in_mins=30, name="Assign_workbook", parameters=parameters, response_types=response_types, callback=check_prompt_response)

    return

def prompt_format(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('prompt_format() called')
    
    results_data_1 = phantom.collect2(container=container, datapath=['get_workbook_templates:action_result.data.*.response_body.data'], action_results=results)
    results_item_1_0 = [item[0] for item in results_data_1]

    prompt_format__user_id = None
    prompt_format__menu_prompt = None

    ################################################################################
    ## Custom Code Start
    ################################################################################
    # Gets the effective playbook user id
    pb_info = phantom.get_playbook_info()
    phantom.debug("Retreving owner name: {0}".format(pb_info[0]["effective_user_id"]))
    prompt_format__user_id = pb_info[0]["effective_user_id"]
    
    if prompt_format__user_id == "2":
        prompt_format__user_id = "1"
        phantom.debug("The workbook playbook was called and by automation without an appropriate tag. Assigning to administrator.")

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key='prompt_format:user_id', value=json.dumps(prompt_format__user_id))
    phantom.save_run_data(key='prompt_format:menu_prompt', value=json.dumps(prompt_format__menu_prompt))
    user_url_format(container=container)

    return

def get_user_name(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('get_user_name() called')
        
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'get_user_name' call
    formatted_data_1 = phantom.get_format_data(name='user_url_format')

    parameters = []
    
    # build parameters list for 'get_user_name' call
    parameters.append({
        'headers': "",
        'location': formatted_data_1,
        'verify_certificate': False,
    })

    phantom.act(action="get data", parameters=parameters, assets=['phantom_rest_api'], callback=Assign_workbook, name="get_user_name")

    return

"""
Remove the json.loads() from create_template
"""
def prompted_workflow_template(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('prompted_workflow_template() called')
    
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    create_template_format__template = phantom.get_run_data(key='create_template_format:template')
    # collect data for 'prompted_workflow_template' call
    formatted_data_1 = phantom.get_format_data(name='container_url_format')

    parameters = []
    
    # build parameters list for 'prompted_workflow_template' call
    parameters.append({
        'location': formatted_data_1,
        'body': create_template_format__template,
        'headers': "",
        'verify_certificate': False,
    })

    phantom.act("post data", parameters=parameters, assets=['phantom_rest_api'], callback=get_workbook_phases, name="prompted_workflow_template")

    return

def check_prompt_response(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('check_prompt_response() called')

    # check for 'if' condition 1
    matched = phantom.decision(
        container=container,
        action_results=results,
        conditions=[
            ["Assign_workbook:action_result.status", "==", "success"],
        ])

    # call connected blocks if condition 1 matched
    if matched:
        create_template_format(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)
        return

    # call connected blocks for 'else' condition 2
    join_missing_workbook_tag(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)

    return

def create_template_format(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('create_template_format() called')
    
    results_data_1 = phantom.collect2(container=container, datapath=['get_workbook_templates:action_result.data.*.response_body.data'], action_results=results)
    results_data_2 = phantom.collect2(container=container, datapath=['Assign_workbook:action_result.summary.responses'], action_results=results)
    results_item_1_0 = [item[0] for item in results_data_1]
    results_item_2_0 = [item[0] for item in results_data_2]

    create_template_format__template = None

    ################################################################################
    ## Custom Code Start
    ################################################################################
    # Create Workbook id holder
    wb_id = 0
    # Display Response results
    #phantom.debug(results_item_2_0)
    case = results_item_2_0[0][0]
    template = results_item_2_0[0][1]
    phantom.debug("Analyst responded to create case? {}".format(case))
    #phantom.debug(results_item_2_0[0][1])
    phantom.debug("Analyst selected template: {}".format(template))
    
    # Based on responses configure case and/or workbook
    if case == "Yes" and template == "None":
        success, message = phantom.promote()
        phantom.debug('phantom.promote results: success: {}, message: {}'.format(success, message))
    elif case == "No" and template == "None":
        phantom.debug('Exiting workbook playbook: Create Case: {}, Template Selected: {}'.format(case, template))
    else:
        for item in results_data_1[0][0]:
            #phantom.debug(item)
            if template == item['name']:
                phantom.debug(item["name"])
                wb_id = item['id']
                create_template_format__template = {"template_id": wb_id}
        if case == "Yes" and template != "None":
            success, message = phantom.promote(template=template)
            phantom.debug('phantom.promote results: success: {}, message: {}'.format(success, message))
    
    #phantom.debug(create_template_format__template)

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key='create_template_format:template', value=json.dumps(create_template_format__template))
    check_for_template(container=container)

    return

def check_for_template(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('check_for_template() called')

    # check for 'if' condition 1
    matched = phantom.decision(
        container=container,
        action_results=results,
        conditions=[
            ["create_template_format:custom_function:template", "!=", ""],
        ])

    # call connected blocks if condition 1 matched
    if matched:
        prompted_workflow_template(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)
        return

    # call connected blocks for 'else' condition 2
    join_missing_workbook_tag(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)

    return

def get_set_current_phase(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('get_set_current_phase() called')
    
    create_template_format__template = json.loads(phantom.get_run_data(key='create_template_format:template'))
    results_data_1 = phantom.collect2(container=container, datapath=['get_workbook_phases:action_result.data.*.response_body.data'], action_results=results)
    results_item_1_0 = [item[0] for item in results_data_1]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # If there was an existing phase as current use that phase.. if not set the or added workbook as the current phase at order: 1
    success, message, phase_id, phase_name = phantom.get_phase()
    
    if success == True and phase_id is None:
        phantom.debug(results_data_1[0][0])
        for phase in results_data_1[0][0]:
            if phase['order'] == 1:
                phase_name = phase['name']
                success, message = phantom.set_phase(phase=phase_name)
                phantom.debug('phantom.set_phase results: success: {}, message: {}'\
                              .format(success, message)
                             )
    else:
        phantom.debug(
            'phantom.get_phase results: success: {}, message: {}, phase_id: {}, phase_name: {}'\
            .format(success, message, phase_id, phase_name)
        )

    ################################################################################
    ## Custom Code End
    ################################################################################

    return

def get_workbook_phases(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('get_workbook_phases() called')
        
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'get_workbook_phases' call
    formatted_data_1 = phantom.get_format_data(name='container_phases_format')

    parameters = []
    
    # build parameters list for 'get_workbook_phases' call
    parameters.append({
        'headers': "",
        'location': formatted_data_1,
        'verify_certificate': False,
    })

    phantom.act(action="get data", parameters=parameters, assets=['phantom_rest_api'], callback=get_set_current_phase, name="get_workbook_phases", parent_action=action)

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