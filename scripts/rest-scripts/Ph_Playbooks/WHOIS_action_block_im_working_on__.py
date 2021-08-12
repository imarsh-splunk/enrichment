def whois_SRC_IP(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('whois_SRC_IP() called')

    # collect data for 'whois_SRC_IP' call
    filtered_artifacts_data_1 = phantom.collect2(container=container, datapath=['filtered-data:filter_1:condition_3:artifact:*.cef.sourceAddress', 'filtered-data:filter_1:condition_3:artifact:*.id'])

    parameters = []
    
    # build parameters list for 'whois_SRC_IP' call
    for filtered_artifacts_item_1 in filtered_artifacts_data_1:
        if filtered_artifacts_item_1[0]:
            parameters.append({
                'ip': filtered_artifacts_item_1[0],
                # context (artifact id) is added to associate results with the artifact
                'context': {'artifact_id': filtered_artifacts_item_1[1]},
            })

    phantom.act("whois ip", parameters=parameters, assets=['whois'], callback=pin_3, name="whois_SRC_IP")

    return