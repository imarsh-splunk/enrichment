import phantom.rules as phantom
import json

# Callback function
def list_vms_cb(action, success, container, results, handle):
    if not success:
        return
    return

# New container or artifact logic function
def on_start(incident):
	# run 'list vms' action on asset by name
	phantom.act('list vms', assets=["vmwarevsphere"], callback=list_vms_cb)
	# run 'list vms' action on assets with 'virtual' tag
	phantom.act('list vms', tags=["virtual"], callback=list_vms_cb)
    return

# After all actions are finished final function
def on_finish(container, summary):
	# Write debug summary log
    phantom.debug(summary)
    return
