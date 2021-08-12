"""
This playbook should be run as a sub-playbook at the end of automation to report its findings. It is an example of how Phantom can be used to generate tickets.
"""

import phantom.rules as phantom
import json
from datetime import datetime, timedelta
def on_start(container):
    phantom.debug('on_start() called')

    return

def Comment_Misconfigured_List(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('Comment_Misconfigured_List() called')

    phantom.comment(container=container, comment="Custom list not configured, or badly configured")

    return

def create_JIRA_ticket(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('create_JIRA_ticket() called')

    name_value = container.get('name', None)

    # collect data for 'create_JIRA_ticket' call

    parameters = []
    
    # build parameters list for 'create_JIRA_ticket' call
    parameters.append({
        'fields': "",
        'summary': name_value,
        'assignee': "",
        'priority': "",
        'vault_id': "",
        'issue_type': "Request new software",
        'description': "Phantom Handled this ticket",
        'project_key': "PRIN",
        'assignee_account_id': "",
    })

    phantom.act(action="create ticket", parameters=parameters, assets=['jira'], callback=JIRA_Status_Message, name="create_JIRA_ticket")

    return

def JIRA_Status_Message(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('JIRA_Status_Message() called')
    
    template = """JIRA Ticket Creation status : {0}"""

    # parameter list for template variable replacement
    parameters = [
        "create_JIRA_ticket:action_result.status",
    ]

    phantom.format(container=container, template=template, parameters=parameters, name="JIRA_Status_Message")

    add_comment_7(container=container)

    return

def add_comment_7(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('add_comment_7() called')

    formatted_data_1 = phantom.get_format_data(name='JIRA_Status_Message')

    phantom.comment(container=container, comment=formatted_data_1)

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