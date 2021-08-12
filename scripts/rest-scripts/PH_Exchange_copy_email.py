def copy_email_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('copy_email_1() called')

    # collect data for 'copy_email_1' call
    container_data = phantom.collect2(container=container, datapath=['artifact:*.cef.emailId', 'artifact:*.cef.toEmail', 'artifact:*.cef.emailHeaders.X-MS-Exchange-Organization-AuthAs', 'artifact:*.id'])

    parameters = []
    
    # build parameters list for 'copy_email_1' call
    for container_item in container_data:
        if container_item[0] and container_item[1] and container_item[2] == 'Internal':
            
            # print collected CEF fields
            phantom.debug(container_item[0])
            phantom.debug(container_item[1])
            phantom.debug(container_item[2])
            
            parameters.append({
                'id': container_item[0],
                # strip the toEmail CEF field to only append 'user@domain.com' to the parameters list
                'email': re.search(r'<(.*?)>', container_item[1]).group(1),
                'folder': "Drafts",
                'impersonate_email': "",
                'dont_impersonate': "",
                # context (artifact id) is added to associate results with the artifact
                'context': {'artifact_id': container_item[3]},
            })

    phantom.act("copy email", parameters=parameters, assets=['exchange'], name="copy_email_1")

    return