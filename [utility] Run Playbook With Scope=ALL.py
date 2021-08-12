"""
This playbook demonstrates how to call a playbook so that it sees all the artifacts (scope=all) when executing. This is good for running a playbook multiple times and scope is not allowing to see all the objects.
"""

import phantom.rules as phantom
import json
from datetime import datetime, timedelta
def on_start(container):
    phantom.debug('on_start() called')
    
    # call 'Configuration' block
    Configuration(container=container)

    return

def Run_Playbook(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('Run_Playbook() called')

    # collect data for 'Run_Playbook' call
    formatted_data_1 = phantom.get_format_data(name='Fornat_REST_Call_Body')

    parameters = []
    
    # build parameters list for 'Run_Playbook' call
    parameters.append({
        'body': formatted_data_1,
        'headers': "",
        'location': "/rest/playbook_run",
        'verify_certificate': False,
    })

    phantom.act("post data", parameters=parameters, assets=['phantom rest api'], name="Run_Playbook")

    return

def Fornat_REST_Call_Body(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('Fornat_REST_Call_Body() called')
    
    template = """{{
  \"container_id\": {0},
  \"playbook_id\": \"{1}\",
  \"scope\": \"all\",
  \"run\": true
}}"""

    # parameter list for template variable replacement
    parameters = [
        "container:id",
        "Configuration:custom_function:Target_Playbook_Name",
    ]

    phantom.format(container=container, template=template, parameters=parameters, name="Fornat_REST_Call_Body")

    Run_Playbook(container=container)

    return

def Configuration(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('Configuration() called')
    input_parameter_0 = ""

    Configuration__Target_Playbook_Name = None

    ################################################################################
    ## Custom Code Start
    ################################################################################

    Configuration__Target_Playbook_Name = "local/dummy playbook"

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key='Configuration:Target_Playbook_Name', value=json.dumps(Configuration__Target_Playbook_Name))
    Fornat_REST_Call_Body(container=container)

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