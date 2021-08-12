def get_run_data(key=None, flatten_lists=None, **kwargs):
    """
    Takes a key name and splits the output for easier access for actions downstream
    
    Args:
        key (CEF type: *): A text string that represents the name of the key saved for a save_run_data() call
        flatten_lists
    
    Returns a JSON-serializable object that implements the configured data paths:
        *.output
    """
    ############################ Custom Code Goes Below This Line #################################
    import json
    import phantom.rules as phantom
    
    outputs = []
    
    def flatten(input_list):
        if not input_list:
            return input_list
        if isinstance(input_list[0], list):
            return flatten(input_list[0]) + flatten(input_list[1:])
        return input_list[:1] + flatten(input_list[1:])
    
    if isinstance(flatten_lists, str) and flatten_lists.lower() in ['y', 'yes', 't', 'true']:
        flatten_lists = True
    elif isinstance(flatten_lists, str) and flatten_lists.lower() in ['n', 'no', 'f', 'false']:
        flatten_lists = False
    elif not flatten_lists:
        flatten_lists = False
    
    
    fetched_data = phantom.get_run_data(key=key)
    if fetched_data:
        try:
            data_as_json = json.loads(fetched_data)
            if isinstance(data_as_json, str):
                outputs.append({'output': data_as_json})
            elif isinstance(data_as_json, dict):
                for k,v in data_as_json.items():
                    outputs.append({'output': {k: v}})
            elif isinstance(data_as_json, list):
                if flatten_lists:
                    data_as_json = flatten(data_as_json)
                for item in data_as_json:
                    outputs.append({'output': item})
        except Exception as e:
            phantom.debug(f"Passing key straight to output due to exception: '{e}'")
            outputs.append({'output': fetched_data})
    else:
        raise RuntimeError(f"No data for key: '{key}'")
        
    # Return a JSON-serializable object
    assert json.dumps(outputs)  # Will raise an exception if the :outputs: object is not JSON-serializable
    return outputs
