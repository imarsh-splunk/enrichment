def delete_email_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('delete_email_2() called')
    
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'delete_email_2' call
    results_data_1 = phantom.collect2(container=container, datapath=['run_query_1:action_result.data.*.t_ItemId.@Id', 'run_query_1:action_result.parameter.context.artifact_id'], action_results=results)

    phantom.debug(results_data_1)
    
    parameters = []
    
    # build parameters list for 'delete_email_2' call
    for results_item_1 in results_data_1:
        if results_item_1[0]:
            parameters.append({
                'id': results_item_1[0],
                'email': "",
                # context (artifact id) is added to associate results with the artifact
                'context': {'artifact_id': results_item_1[1]},
            })
    
    phantom.debug(parameters)
    
    #phantom.act("delete email", parameters=parameters, assets=['ews_o365'], name="delete_email_2", parent_action=action)

    return