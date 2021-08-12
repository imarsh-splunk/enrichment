def parse_unique_artifacts(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('parse_unique_artifacts() called')
    
    # collect data from 'phish@cnb.com' To Address filter block call
    body_results = phantom.collect2(container=container, datapath=['filtered-data:phishMe_email_filter:condition_1:artifact:*.cef.bodyText'])
    
    # Define list of matched "Link text: X URL: X Domain: X" results
    match_list = re.findall(r'Link text: (.*?)\nURL: (.*?)\nURL Domain: (.*?)\n', body_results[0][0], re.DOTALL)     
    
    all_urls = []
    all_domains = []
    
    for match in match_list:
        if not match[1].startswith("http"):
            continue
            
        all_urls.append(match[1].replace("[.]", "."))
        all_domains.append(match[2].replace("[.]", "."))
    
    unique_urls = list(set(all_urls))
    unique_domains = list(set(all_domains))
    
    # Create blank dictionaries to append found URLs/Domains to
    raw = {}
    cef = {}
    
    # Strip out any 'protect2.fireeye.com' URL prefixes
    for url in unique_urls:
        if 'protect2.fireeye.com' in url:
            phantom.debug('url before: {}'.format(url))
            url = re.findall(r'u=(.*)', url)[0]
            phantom.debug('url after: {}'.format(url))
            
        # Add only unique and filtered URLs into the single-key CEF dictionary
        cef['requestURL'] = url
        
        # Add a new URL Artifact for each URL found
        phantom.add_artifact(container=container, raw_data=raw, cef_data=cef, label='url', name='URL Artifact', severity='medium', identifier=None, artifact_type='url')
    
    #Clear CEF dictionary
    del cef['requestURL']

    for domain in unique_domains:
        if 'protect2.fireeye.com' not in domain:
            
            # Add only unique and filtered Domains into the single-key CEF dictionary
            cef['destinationDnsDomain'] = domain
            
            # Add a new Domain Artifact for each Domain found 
            phantom.add_artifact(container=container, raw_data=raw, cef_data=cef, label='domain', name='Domain Artifact', severity='medium', identifier=None, artifact_type='domain')
    
    return