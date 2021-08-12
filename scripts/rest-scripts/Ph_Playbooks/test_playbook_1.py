import phantom.rules as phantom
import json
from datetime import datetime, timedelta
import requests
import time
import re

def on_start(container):
    PHANTOM_TOKEN = ‘XXXXXX’
    modContainerstatus(PHANTOM_TOKEN,container.get(‘id’),‘open’)
    data = processData(container)

    if data != None:
        getIncident(data)

        #tryAgain = True
        #counter = 0

        #while tryAgain:
        #    time.sleep(10)
        #    if counter >= 8:
        #        break
        #    else:
        #        if phantom.completed([‘run query’]):
        #            tryAgain = False
        #            phantom.debug(‘check’)
        #    counter +=1


        #routineCheck = True
        #while routineCheck:
        #    if phantom.completed([‘run query’]):
        #        routineCheck = False
        #    phantom.debug(‘checked’)
        #    time.sleep(6)

        #artifactData = phantom.get_data(str(container.get(‘id’)),clear_data=True)

        #postArtifacts(PHANTOM_TOKEN, container.get(‘id’), artifactData)
    return

def processData(container):

    def stringCleaner(s):

        badChars = [‘<’, ‘>’, ‘\\‘, ‘;’ ]
        for char in range(len(badChars)):
            s = s.replace(badChars[char],‘’)

        return s

    try:
        data=phantom.collect2(container=container,datapath=[‘artifact:*.cef.messageID’,‘artifact:*.cef.recipient’], scope=‘all’)
    except:
        phantom.debug(‘Something Went Wrong’)

    pData = []
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] != None and type(data[i][j]) is str:
                cleanStr = stringCleaner(data[i][j])
                tempDict = {‘msgId’ : cleanStr}
                pData.append(tempDict)
            elif data[i][j] != None and type(data[i][j]) is list:
                cleanStr = stringCleaner(data[i][j][0])
                if re.match(r”[^@]+@[^@]+\.[^@]+“, cleanStr):
                    tempDict = {‘toAdd’ : cleanStr}
                    pData.append(tempDict)

    if pData == []:
        pData = None

    return pData


def getIncident(data):
    parameters = []
    messageId = ‘’
    toAddress = ‘’

    for i in range(len(data)):
        if ‘msgId’ in data[i].keys():
            messageId = data[i][‘msgId’]

        elif ‘toAdd’ in data[i].keys():
            toAddress = data[i][‘toAdd’]

    query = ‘index=“pptrap_hulu_com” sourcetype=“proofpoint_trap” quarantineResults=*%s* *%s* earliest=-3600m latest=now()’ % (messageId, toAddress)
    parameters = [{‘query’ : query}]

    phantom.act(‘run query’, parameters=parameters, assets=[‘splunk_es’], callback=processIncidentresults)

    return

def processIncidentresults(action, success, container, results, handle):
    quarantineResults = ‘’

    if results[0][‘action_results’][0][‘status’] == ‘success’ and results[0][‘action_results’][0][‘data’] != []:
        quarantineResults = ‘’
        try:
            searchData = results[0][‘action_results’][0][‘data’]
            quarantineStatus = searchData[0][‘quarantineResults’]
            phantom.debug(quarantineStatus)
        except:
            phantom.debug(‘Could not parse quarantine status’)

        if quarantineResults:
            quarantineResults = json.loads(quarantineResults)

    else:
        quarantineResuts = None

    phantom.save_data(quarantineResults, key=str(container.get(‘id’)) )

    return

def modContainerstatus(phantomToken, containerId,status):
    URL = ‘https://10.86.16.202/rest/container/’
    headers = {‘ph-auth-token’: phantomToken}

    ID = str(containerId)
    status = str(status)
    body =‘{“status”: “%s”}’ %(status)

    URL = URL + ID

    req = requests.post(URL, headers=headers,data=body,verify=False)

    return

def postArtifacts(phantomToken, containerId, artifactData):
    customFields = ‘’
    URL = "https://XXXXX/rest/artifact/"

    headers = {‘ph-auth-token’: phantomToken}

    for item in artifactData:
        customFields += “%s : %s” % (item, artifactData[item])
    customFields = customFields[:-2]

    TEMPLATE = ‘{“container_id”: %d ,“name” : “%s”,“label”: “event”, “source_data_identifier” :“%s”,“severity”: “%s”, “cef”:{%s}, “run_automation”: “False”}’ % (containerId, ‘TRAP Quarantine Result’,‘1337hax0r’,‘Medium’,customFields)

    req = requests.post(URL,headers=headers, data=TEMPLATE, verify=False)
    phantom.debug(req)
    phantom.debug(req.raise_for_status())
    return

def on_finish(container, summary):
    phantom.debug(‘on_finish() called’)


    return 