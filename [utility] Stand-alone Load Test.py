"""
This just a load testing playbook that runs 4 actions and with ~6 second delays
"""

import phantom.rules as phantom
import json
from datetime import datetime, timedelta
def on_start(container):
    phantom.debug('on_start() called')
    
    # call 'set_status_2' block
    set_status_2(container=container)

    return

def no_op_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('no_op_1() called')

    # collect data for 'no_op_1' call

    parameters = []
    
    # build parameters list for 'no_op_1' call
    parameters.append({
        'sleep_seconds': "2",
    })

    phantom.act("no op", parameters=parameters, assets=['phantom'], callback=geolocate_ip_1, name="no_op_1")

    return

def geolocate_ip_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('geolocate_ip_1() called')
    
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'geolocate_ip_1' call

    parameters = []
    
    # build parameters list for 'geolocate_ip_1' call
    parameters.append({
        'ip': "1.1.1.1",
    })

    phantom.act("geolocate ip", parameters=parameters, assets=['maxmind'], callback=no_op_2, name="geolocate_ip_1", parent_action=action)

    return

def no_op_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('no_op_2() called')
    
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'no_op_2' call

    parameters = []
    
    # build parameters list for 'no_op_2' call
    parameters.append({
        'sleep_seconds': "2",
    })

    phantom.act("no op", parameters=parameters, assets=['phantom'], callback=no_op_3, name="no_op_2", parent_action=action)

    return

def no_op_3(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('no_op_3() called')
    
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'no_op_3' call

    parameters = []
    
    # build parameters list for 'no_op_3' call
    parameters.append({
        'sleep_seconds': "2",
    })

    phantom.act("no op", parameters=parameters, assets=['phantom'], callback=set_status_1, name="no_op_3", parent_action=action)

    return

def set_status_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('set_status_1() called')

    phantom.set_status(container=container, status="Closed")

    return

def set_status_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('set_status_2() called')

    phantom.set_status(container=container, status="Open")
    no_op_1(container=container)

    return

def on_finish(container, summary):
    phantom.debug('on_finish() called')
    # This function is called after all actions are completed.
    # summary of all the action and/or all detals of actions
    # can be collected here.

    # summary_json = phantom.get_summary()
    # if 'result' in summary_json:
        # for action_result in summary_json['result']:
            # if 'action_run_id' in action_result:
                # action_results = phantom.get_action_results(action_run_id=action_result['action_run_id'], result_data=False, flatten=False)
                # phantom.debug(action_results)

    return