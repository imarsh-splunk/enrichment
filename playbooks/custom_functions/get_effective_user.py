def get_effective_user(**kwargs):
    """
    Retrieve effective user in a running playbook
    
    Returns a JSON-serializable object that implements the configured data paths:
        username: username
        effective_user_id: user id
    """
    ############################ Custom Code Goes Below This Line #################################
    import json
    import phantom.rules as phantom
    
    outputs = {}
    # Write your custom code here...
    effective_user_id = phantom.get_effective_user()
    url = 'https://127.0.0.1/rest/ph_user/{}'.format(effective_user_id)
    r = phantom.requests.get(url, verify=False)
    resp_json = r.json()
    username = resp_json.get('username')
    
    outputs = {
        'effective_username': username,
        'effective_user_id': effective_user_id
    }
    
    # Return a JSON-serializable object
    assert json.dumps(outputs)  # Will raise an exception if the :outputs: object is not JSON-serializable
    return outputs
