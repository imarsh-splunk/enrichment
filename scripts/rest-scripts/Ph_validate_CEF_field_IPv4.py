def vt_dest_ip_reputation(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('vt_dest_ip_reputation() called')

    # collect data for 'vt_dest_ip_reputation' call
    filtered_artifacts_data_1 = phantom.collect2(container=container, datapath=['filtered-data:filter_4:condition_1:artifact:*.cef.destinationAddress', 'filtered-data:filter_4:condition_1:artifact:*.id'])
    
    parameters = []
    
    # build parameters list for 'vt_dest_ip_reputation' call
    for filtered_artifacts_item_1 in filtered_artifacts_data_1:
        if filtered_artifacts_item_1[0]:
            
            valid_ip = phantom.valid_ip(filtered_artifacts_item_1[0])
            
            if valid_ip == 'True':
                
                parameters.append({
                    'ip': phantom.valid_ip(filtered_artifacts_item_1[0]),
                    # context (artifact id) is added to associate results with the artifact
                    'context': {'artifact_id': filtered_artifacts_item_1[1]},
                })

    if parameters:
    
        phantom.act("ip reputation", parameters=parameters, app={ "name": 'VirusTotal' }, name="vt_dest_ip_reputation")

    return