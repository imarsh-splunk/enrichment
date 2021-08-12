    phantom.debug('copy_custom_list_to_file() called')

    # collect data for 'copy_custom_list_to_file' call

    parameters = []
    # Start custom code block
    list_name = 'test'
    success, message, custom_list = phantom.get_list(list_name)
    cl_json = json.dumps({list_name: custom_list}, indent=4)
    if not success:
        # End the block before making changes, which will end the playbook
        # It is also possible to use this time to delete an existing file using the 'delete file' action
        return
    # End custom code block
    
    # build parameters list for 'copy_custom_list_to_file' call
    parameters.append({
        'file_path': "file_name_to_use.json",
        'contents': cl_json,  # Add custom list variable from above here
        'vault_id': "",
    })

    phantom.act("add file", parameters=parameters, assets=['github'], callback=git_status, name="copy_custom_list_to_file")
