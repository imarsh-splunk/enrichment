

filtered_artifacts_data_1 = phantom.collect2(container=container, datapath=['filtered-data:filter_1:condition_1:artifact:*.cef'])
filtered_artifacts_item_1_0 = [item[0] for item in filtered_artifacts_data_1]




# Find and replace any JSON Keys which have a "." or "::" in them to have an underscore
    for k, v in notable_artifact_json.iteritems():
        if "." in k or "::" in k or "(" in k or ")" or "{}" in k:
            new_key = k.replace('.', '_').replace('::', '_').replace('(', '_').replace(')', '_').replace('{}', '')
            notable_artifact_json[new_key] = notable_artifact_json.pop(k)
    # Add "Notable Event Artifact" to Phantom Event
    success, message, artifact_id = phantom.add_artifact(container=container['id'], 
                                                          raw_data={}, 
                                                          cef_data=notable_artifact_json, 
                                                          label="notable", 
                                                          name="Notable Event Artifact", 
                                                          severity="medium", 
                                                          identifier=None, 
                                                          artifact_type="notable", 
                                                          field_mapping=None, 
                                                          trace=False, 
                                                          run_automation=False)

