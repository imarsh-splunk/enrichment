"""
This playbook finds related containers based upon their indicator values. It formats that data into an easy-to-digest report with links for the analyst in a dynamically generated prompt. Once the analyst decides to merge the containers, the process_container_merge function copies the data over from the child containers and closes them out. Finally, any event_ids found in the containers are updated with their new status and links to the parent case.
"""

import phantom.rules as phantom
import json
from datetime import datetime, timedelta
def on_start(container):
    phantom.debug('on_start() called')
    
    # call 'cf_phantom_riskanalysis_pack_find_related_containers_1' block
    cf_phantom_riskanalysis_pack_find_related_containers_1(container=container)

    return

"""
Check if the previous function returned any values
"""
def containers_exist(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('containers_exist() called')

    # check for 'if' condition 1
    matched = phantom.decision(
        container=container,
        action_results=results,
        conditions=[
            ["cf_phantom_riskanalysis_pack_find_related_containers_1:custom_function_result.data.*.container_id", "!=", ""],
        ])

    # call connected blocks if condition 1 matched
    if matched:
        get_effective_user(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)
        return

    return

"""
Get the user that launched the playbook. This will return a real user or an automation user.
"""
def get_effective_user(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('get_effective_user() called')
    
    input_parameter_0 = ""

    get_effective_user__username = None

    ################################################################################
    ## Custom Code Start
    ################################################################################

    effective_user_id = phantom.get_effective_user()
    url = phantom.build_phantom_rest_url('ph_user', effective_user_id)
    get_effective_user__username = phantom.requests.get(url, verify=False).json().get('username')

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key='get_effective_user:username', value=json.dumps(get_effective_user__username))
    custom_format(container=container)

    return

"""
Prompt the user who launched this playbook with the full report so they can select the containers to merge.  Limited to 20 events - future state will allow more. It also builds a dynamic merge which is why it has custom code.
"""
def merge_containers(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('merge_containers() called')
    
    # set user and message variables for phantom.prompt call
    user = json.loads(phantom.get_run_data(key='get_effective_user:username'))
    message = """{0}"""

    # parameter list for template variable replacement
    parameters = [
        "custom_format:custom_function:output",
    ]
    
    # fetch data for dynamic response
    container_data = phantom.collect2(container=container, datapath=['cf_phantom_riskanalysis_pack_find_related_containers_1:custom_function_result.data.*.container_id'], action_results=results)
    container_list = [item[0] for item in container_data]
    
    #Dynamic Responses:
    response_types = []
    for item in container_list:
        response_types.append({
                "prompt": "Merge {}?".format(item),
                "options": {
                    "type": "list",
                    "choices": [
                        "Yes",
                        "No",
                    ]
                },
            })
        
    phantom.save_run_data(value=json.dumps(container_list), key="container_list", auto=True)    
    
    phantom.prompt2(container=container, user=user, message=message, parameters=parameters, respond_in_mins=30, name="merge_containers", response_types=response_types, callback=process_container_merge)

    return

"""
Custom process for merging containers. Each section on what it does for the merge process is documented. Modify at your own risk.
"""
def process_container_merge(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('process_container_merge() called')
    
    input_parameter_0 = ""

    process_container_merge__event_ids = None

    ################################################################################
    ## Custom Code Start
    ################################################################################
    process_container_merge__event_ids = []
    results_data_1 = phantom.collect2(container=container, datapath=['merge_containers:action_result.summary.responses'], action_results=results)
    results_item_1_0 = [item[0] for item in results_data_1]
    
    responses = results_item_1_0[0]
    # Grab run_key and convert to list
    container_list = json.loads(phantom.get_run_data(key='container_list'))
    
    if 'Yes' in responses or 'yes' in responses:
        child_container_list = []
        child_container_name_list = []
        
        # Gather all artifacts from parent_container
        phantom.debug("Gathering all artifacts from parent container")
        url = phantom.build_phantom_rest_url('container', container['id'], 'artifacts')
        request_json = phantom.requests.get(uri=url, verify=False).json()
        parent_cef_list = []
        if request_json['count'] > 0:
            for data in request_json['data']:
                parent_cef_list.append(data['cef'])
                
        #### Prep parent container
        phantom.debug("Prepping parent container")
        # Get parent worbook name
        url = phantom.build_phantom_rest_url('container', container['id'])
        workflow_name = phantom.requests.get(uri=url, verify=False).json().get('workflow_name')
        update_data = {'container_type': 'case'}
        if workflow_name:
            if not '[Parent]' in container['name']:
                update_data['name'] = "[Parent] {}".format(container['name'])
                phantom.update(container, update_data)
            else:
                phantom.update(container, update_data)
        else:
            phantom.debug("Prepping parent container - no workflow exists, adding default workbook")
            phantom.promote(container=container['id'])
            update_data = {'name': "[Parent] {}".format(container['name'])}
            phantom.update(container, update_data)
            
        # Check if current phase is set. If not, set the current phase to the first available phase to avoid artifact merge bug
        if not container.get('current_phase_id'):
            phantom.debug("Phase not set, settings current_phase to first phase")
            url = phantom.build_phantom_rest_url('workbook_phase') + "?_filter_container={}".format(container['id'])
            request_json = phantom.requests.get(uri=url, verify=False).json()
            update_data = {'current_phase_id': request_json['data'][0]['id']}
            phantom.update(container, update_data)
            
        # Iterate through child containers
        for child_container_id,response in zip(container_list, responses):
            event_id = phantom.collect2(container=phantom.get_container(child_container_id), datapath=['artifact:*.cef.event_id'], scope='all')
            for value in event_id:
                if value:
                    process_container_merge__event_ids.append(value)
            
            if response.lower() == 'yes':
                phantom.debug("Processing Child Container ID: {}".format(child_container_id))
                child_container_list.append(child_container_id)
                child_container_name = (phantom.get_container(child_container_id).get('name'))
                child_container_name_list.append(child_container_name)
                
                # Update container name with parent relationship
                if not "[Parent:" in child_container_name:
                    update_data = {'name': "[Parent: {0}] {1}".format(container['id'], child_container_name)}
                    phantom.update(phantom.get_container(child_container_id), update_data)
                
                # Gather artifacts for child container
                phantom.debug("Gathering artifacts for child container {}".format(child_container_id))
                url = phantom.build_phantom_rest_url('container', child_container_id, 'artifacts') 
                request_json = phantom.requests.get(uri=url, verify=False).json()
                if request_json['count'] > 0:
                    for data in request_json['data']:
                        # Compare child artifacts to parent artifacts. Only merge them if they are not the same
                        for parent_cef in parent_cef_list:
                            if parent_cef != data['cef'] and 'event_id' not in data['cef'].keys():
                                phantom.merge(case=container['id'], artifact_id=data['id'])
                
                #Gather notes for child container
                phantom.debug("Gathering notes for child container '{}'".format(child_container_id))
                for note in phantom.get_notes(container=child_container_id):
                    if note['success'] and not note['data']['title'] in ('[Auto-Generated] Related Containers', 
                                                                         '[Auto-Generated] Parent Container', 
                                                                         '[Auto-Generated] Child Containers'):
                        phantom.debug("Adding note: '{}'".format(note['data']['title']))
                        phantom.add_note(container=container['id'],
                                         note_type='general',
                                         note_format=note['data']['note_format'],
                                         title="[From Event {0}] {1}".format(note['data']['container'], note['data']['title']),
                                         content=note['data']['content'])

                # Perform final cleanup on child container
                phantom.debug("Adding parent relationship note to child container '{}'".format(child_container_id))
                success, message, child_note_id = phantom.add_note(container=child_container_id,
                                 note_type="general",
                                 note_format="markdown",
                                 title="[Auto-Generated] Parent Container",
                                 content="| Container_ID | Container_Name |\n| --- | --- |\n| {0} | [{1}]({2}/mission/{0}) |".format(container['id'], container['name'], phantom.get_base_url()))
                # Mark child note as evidence
                data = {
                    "container_id": child_container_id,
                    "object_id": child_note_id,
                    "content_type": "note"
                }
                url = phantom.build_phantom_rest_url('evidence')
                response = phantom.requests.post(uri=url, json=data, verify=False).json()
                phantom.set_status(container=child_container_id, status="closed")
                
                # Mark child container as evidence in parent container:
                data = {
                    "container_id": container['id'],
                    "object_id": child_container_id,
                    "content_type": "container"
                }
                url = phantom.build_phantom_rest_url('evidence')
                response = phantom.requests.post(uri=url, json=data, verify=False).json()

        # Format note for link back to child_containers in parent_container
        phantom.debug("Adding list of child containers to parent note")
        format_list = []
        for child_container_id,child_container_name in zip(child_container_list,child_container_name_list):
            format_list.append("| {0} | [{1}]({2}/mission/{0}) |\n".format(child_container_id, child_container_name, phantom.get_base_url()))
            
        # Fetch pevious 
        url = phantom.build_phantom_rest_url('note') + '?_filter_container="{}"&_filter_title="[Auto-Generated] Child Containers"'.format(container['id'])
        response_data = phantom.requests.get(url, verify=False).json()
        # If old notes exist proceed to overwrite, else add new note
        note_title = "[Auto-Generated] Child Containers"
        note_format = "markdown"
        if response_data['count'] > 0:
            phantom.debug("Existing 'Child Container' Note found")
            for item in response_data['data']:
                # Check to see if this has been done before, if so append it to existing note.
                if item.get('title') and note_title == item.get('title'):
                    note_content = item['content'] + "\n"
                    phantom.debug("Updating previous 'Child Containers' Note")
                    for c_note in format_list:
                        note_content += c_note
                    data = {"note_type": "general",
                            "title": note_title,
                            "content": note_content,
                            "note_format": note_format}
                    url = phantom.build_phantom_rest_url('note')
                    response_data = phantom.requests.post(url + "/{}".format(item['id']), json=data, verify=False).json()
                    
        else:
            phantom.debug("Adding new note for 'Child Containers'")
            template = "| Container ID | Container Name |\n| --- | --- |\n"
            for c_note in format_list:
                template += c_note
            success, message, process_container_merge__note_id = phantom.add_note(container=container, 
                                                                                  note_type="general", 
                                                                                  title=note_title, 
                                                                                  content=template, 
                                                                                  note_format=note_format)

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key='process_container_merge:event_ids', value=json.dumps(process_container_merge__event_ids))
    cf_phantom_riskanalysis_pack_get_run_data_1(container=container)

    return

"""
Get a list of all events on the platform NOT status "closed" that have at least the minimum_match_count in common with this event. The "*" allows you to check against all data paths instead of just one.
"""
def cf_phantom_riskanalysis_pack_find_related_containers_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('cf_phantom_riskanalysis_pack_find_related_containers_1() called')
    
    container_property_0 = [
        [
            container.get("id"),
        ],
    ]
    literal_values_0 = [
        [
            "*",
            "closed",
            3,
        ],
    ]

    parameters = []

    literal_values_0_0 = [item[0] for item in literal_values_0]

    for item0 in container_property_0:
        for item1 in literal_values_0:
            parameters.append({
                'container': item0[0],
                'value_list': literal_values_0_0,
                'filter_out_status': item1[1],
                'minimum_match_count': item1[2],
            })
    ################################################################################
    ## Custom Code Start
    ################################################################################

    ################################################################################
    ## Custom Code End
    ################################################################################    

    # call custom function "phantom_riskanalysis_pack/find_related_containers", returns the custom_function_run_id
    phantom.custom_function(custom_function='phantom_riskanalysis_pack/find_related_containers', parameters=parameters, name='cf_phantom_riskanalysis_pack_find_related_containers_1', callback=containers_exist)

    return

"""
Produce a custom format that calculates how many related indicators there are per container. This is used to truncate the output if its over the specified amount.
"""
def custom_format(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('custom_format() called')
    
    custom_function_results_data_1 = phantom.collect2(container=container, datapath=['cf_phantom_riskanalysis_pack_find_related_containers_1:custom_function_result.data.*.container_id', 'cf_phantom_riskanalysis_pack_find_related_containers_1:custom_function_result.data.*.indicator_id', 'cf_phantom_riskanalysis_pack_find_related_containers_1:custom_function_result.data.*.container_name'], action_results=results)
    custom_function_results_item_1_0 = [item[0] for item in custom_function_results_data_1]
    custom_function_results_item_1_1 = [item[1] for item in custom_function_results_data_1]
    custom_function_results_item_1_2 = [item[2] for item in custom_function_results_data_1]

    custom_format__output = None

    ################################################################################
    ## Custom Code Start
    ################################################################################
    # Define base format - customize as needed
    custom_format__output = """Please select the events to merge into this one.
This process will:
 - Mark the current event as the parent case. If no workbook has been added, it will use the default workbook.
 - Add events and artifacts to the parent case.
 - Copy all related event notes to the parent case.
 - Mark the other events closed with a link to the parent case\n\n"""
    
    # Build phantom url for use later 
    base_url = phantom.get_base_url()
    url = phantom.build_phantom_rest_url('indicator')
    
    # Iterate through all inputs and append to base format
    for item1,item2,item3 in zip(custom_function_results_item_1_0,custom_function_results_item_1_1,custom_function_results_item_1_2):
        custom_format__output += "#### [Event {0}: {1}]({2}/mission/{0}/summary/evidence)\n".format(item1, item3, base_url)
        
        # If length is greater than 10, truncate
        if len(item2) > 10:
            # Find_related_containers only returns an indicator id, this converts the indicator id to an actual value
            for indicator in item2[0:10]:
                response = phantom.requests.get(uri = url + "/{}".format(indicator), verify=False).json()
                custom_format__output += "- ```{}```\n".format(response.get('value'))
            custom_format__output += "- ***+{} additional related artifacts***".format(len(item2) - 10)
        else:
            for indicator in item2:
                response = phantom.requests.get(uri = url + "/{}".format(indicator), verify=False).json()
                custom_format__output += "- ```{}```\n".format(response.get('value'))
        custom_format__output += "\n---\n\n"

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key='custom_format:output', value=json.dumps(custom_format__output))
    merge_containers(container=container)

    return

"""
Update all event ids from containers that were merged with their latest status
"""
def update_event_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('update_event_1() called')
        
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'update_event_1' call
    custom_function_results_data_1 = phantom.collect2(container=container, datapath=['cf_phantom_riskanalysis_pack_get_run_data_1:custom_function_result.data.*.output'], action_results=results)
    formatted_data_1 = phantom.get_format_data(name='es_format')

    parameters = []
    
    # build parameters list for 'update_event_1' call
    for custom_function_results_item_1 in custom_function_results_data_1:
        if custom_function_results_item_1[0]:
            parameters.append({
                'owner': "",
                'status': "closed",
                'comment': formatted_data_1,
                'urgency': "",
                'event_ids': custom_function_results_item_1[0],
                'integer_status': "",
                'wait_for_confirmation': False,
            })

    phantom.act(action="update event", parameters=parameters, assets=['splunk'], name="update_event_1")

    return

"""
Grab the Notable Event Ids saved key from the previous block and output them in a friendly data path
"""
def cf_phantom_riskanalysis_pack_get_run_data_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('cf_phantom_riskanalysis_pack_get_run_data_1() called')
    
    literal_values_0 = [
        [
            "process_container_merge:event_ids",
            "True",
        ],
    ]

    parameters = []

    for item0 in literal_values_0:
        parameters.append({
            'key': item0[0],
            'flatten_lists': item0[1],
        })
    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################    

    # call custom function "phantom_riskanalysis_pack/get_run_data", returns the custom_function_run_id
    phantom.custom_function(custom_function='phantom_riskanalysis_pack/get_run_data', parameters=parameters, name='cf_phantom_riskanalysis_pack_get_run_data_1', callback=es_format)

    return

"""
Produce final note for posting to ES
"""
def es_format(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('es_format() called')
    
    template = """Event merged into parent case: {0}

Name: {1}

URL: {2}"""

    # parameter list for template variable replacement
    parameters = [
        "container:id",
        "container:name",
        "container:url",
    ]

    phantom.format(container=container, template=template, parameters=parameters, name="es_format")

    update_event_1(container=container)

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