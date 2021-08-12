def run_query_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('run_query_1() called')
    
    # collect data for 'run_query_1' call
    container_data = phantom.collect2(container=container, datapath=['artifact:*.cef.fromEmail', 'artifact:*.cef.emailSubject'])
    sender = container_data[0][0]
    subject = container_data[0][1]
    
    # collect std_out data from Get-MessageTrace cmdlet call
    std_out = phantom.collect2(container=container, datapath=['GetMessageTrace_find_recipients:action_result.data.*.std_out'])
    recipient_list = std_out[0][0].split("\r\n")
    
    parameters = []
    
    for recipient in recipient_list:
        if recipient:
            # build parameters list for 'run_query_1' call
            parameters.append({
                'email': "{0}".format(recipient),
                'folder': "",
                'subject': "{0}".format(subject),
                'sender': "{0}".format(sender),
                'body': "",
                'internet_message_id': "",
                'query': "",
                'range': "0-10",
                'ignore_subfolders': "",
            })
            
    phantom.debug(parameters)        
            
    phantom.act("run query", parameters=parameters, assets=['ews_o365'], callback=delete_email_2, name="run_query_2", parent_action=action)

    return