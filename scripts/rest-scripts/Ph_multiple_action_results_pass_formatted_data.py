def add_comment_3(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('add_comment_3() called')

    results_data_1 = phantom.collect2(container=container, datapath=['run_query:action_result.data.*.ip_address'], action_results=results)

    results_item_1_0 = [item[0] for item in results_data_1]
    
    for item in results_item_1_0:
        if item:
            
            phantom.debug(item)
            
            comment = "This sourceAddress was found on the whitelist: {0}".format(item)

            phantom.comment(container=container, comment=comment)

    return