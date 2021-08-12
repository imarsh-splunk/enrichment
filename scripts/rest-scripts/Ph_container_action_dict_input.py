import phantom.rules as phantom
import json

def whois_domain_cb(action, success, container, results, handle):

    if not success:
        return

    return

def on_start(incident):

    params = []

    hosts = phantom.collect(incident, 'artifact:*.cef.sourceDnsDomain', 'all', 100)
    for host in hosts:
        params.append({ 'domain': host })     

    phantom.act('whois domain', parameters=params, callback=whois_domain_cb)
    return
    