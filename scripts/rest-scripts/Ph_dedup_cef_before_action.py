def run_query(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('run_query() called')

    # collect data for 'run_query' call
    container_data = phantom.collect2(container=container, datapath=['artifact:*.cef.sourceAddress'])
    phantom.debug(container_data)
    
    unique_data = [list(x) for x in set(tuple(x) for x in container_data)]
    phantom.debug(unique_data)
    
    parameters = []
    
    # build parameters list for 'run_query' call
    for container_item in unique_data:
        if container_item[0]:
            
            template = "| inputlookup IP_Whitelist.csv | search ip_address='{0}'".format(container_item[0])
            
            parameters.append({
                'query': template,
                'display': "",
            })
    phantom.debug(parameters)
    phantom.act("run query", parameters=parameters, assets=['splunkenterprise.homelab'], name="run_query")

    return