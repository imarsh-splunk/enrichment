def join_format_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('join_format_1() called')
    fileHashes = phantom.collect2(container=container, datapath=['filtered-data:fileFilter:condition_1:artifact:*.cef.fileHashSha256'])
    phantom.debug('fileHashes: {}'.format(fileHashes))
    
    requestURLs = phantom.collect2(container=container, datapath=['filtered-data:URL_FIlterset:condition_1:artifact:*.cef.requestURL'])
    phantom.debug('requestURLs: {}'.format(requestURLs))
    
    sourceAddresses = phantom.collect2(container=container, datapath=['filtered-data:sourceAddressFilter:condition_1:artifact:*.cef.sourceAddress'])
    phantom.debug('sourceAddresses: {}'.format(sourceAddresses))
    
    dnsDomains = phantom.collect2(container=container, datapath=['filtered-data:destinationDnsDomainFilter:condition_1:artifact:*.cef.destinationDnsDomain'])
    phantom.debug('dnsDomains: {}'.format(dnsDomains))
    if len(fileHashes) > 0:
        phantom.debug('More than 1 result in fileHashes')
        fileHashes_flag = phantom.actions_done(['hunt_file_1'])
    else:
        fileHashes_flag = True
    
    if len(requestURLs) > 0:
        phantom.debug('More than 1 result in requestURLs')
        requestURLs_flag = phantom.actions_done(['get_screenshot_3'])
    else:
        requestURLs_flag = True
    if len(sourceAddresses) > 0:
        phantom.debug('More than 1 result in sourceAddresses')
        sourceAddresses_flag = phantom.actions_done(['domain_reputation_3'])
    else:
        sourceAddresses_flag = True
    
    if len(dnsDomains) > 0:
        phantom.debug('More than 1 result in dnsDomains')
        dnsDomains_flag = phantom.actions_done(['whois_infoDomain'])
    else:
        dnsDomains_flag = True
    # check if all connected incoming actions are done i.e. have succeeded or failed
    if (fileHashes_flag == True) \
        and (requestURLs_flag == True) \
        and (sourceAddresses_flag == True) \
        and (dnsDomains_flag == True):
        
        # call connected block "format_1"
        format_1(container=container, handle=handle)
    
    return