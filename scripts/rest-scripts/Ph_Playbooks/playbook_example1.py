import phantom.rules as phantom
import json
# this is a callback function for the action.
# Evaluate the results and/or call other actions
def geolocate_ip_cb(action, success, container, results, handle):
    # 
    # See the documentation for 'callback' for detailed information on 
    # these parameters
    # 
    if not success:
        return
    return
    
    # This function gets called for all new containers or when new artifacts 
# are added to an existing container. 
def on_start(container):
    # container is a JSON object representing the object that this playbook 
    # can automate on

    # use phantom.collect() API to get the artifacts that belong 
    # to this container and call phantom.act(). 
    
    ips = set(phantom.collect(container, 'artifact:*.cef.sourceAddress'))
    parameters = []
    for ip in ips:
        parameters.append({ "ip" : ip })

    if parameters:
        # In phantom.act(), use the optional parameter 'callback' to get 
        # called when the action completes
        my_test_ips = []
        my_test_ips.append('1.1.1.1')
        phantom.act('geolocate ip', 
                    parameters=parameters, 
                    assets=["maxmind"], 
                    handle=json.dumps(my_test_ips),
                    callback=geolocate_ip_cb)
    return

def on_finish(container, summary):
    # Summary is a user friendly representation of all action outcomes

    # call phantom.get_summary() to get a JSON representation of all
    # action results here
    return






