filtered_artifacts_item_1[0]

container_data = phantom.collect2(container=container, datapath=['artifact:*.cef.fromEmail', 'artifact:*.cef.emailSubject'])

sender = re.search(r'<(.*?)>', container_data[0][0])
subject = container_data[0][1]

