tstats_spl = [
  {
    "status": "success",
    "parameter": {
      "query": "| rest splunk_server=local count=0 /servicesNS/-/-/saved/searches\n| search title=\"ESCU - Detect Long DNS TXT Record Response - Rule\"\n| table title search",
      "display": "title,search",
      "context": {
        "guid": "5fb780ea-4487-4d42-9dd6-61e990a7bb84",
        "artifact_id": 0,
        "parent_action_run": []
      }
    },
    "message": "Total events: 1",
    "data": [
      {
        "search": "| tstats count min(_time) as firstTime max(_time) as lastTime from datamodel=Network_Resolution where DNS.message_type=response AND DNS.record_type=TXT by DNS.src DNS.dest DNS.answer DNS.record_type \n| `drop_dm_object_name(\"DNS\")` \n| eval anslen=len(answer) \n| where anslen>100 \n| `ctime(firstTime)` \n| `ctime(lastTime)` \n| fields src dest answer anslen record_type firstTime lastTime count",
        "title": "ESCU - Detect Long DNS TXT Record Response - Rule"
      }
    ],
    "summary": {
      "total_events": 1
    }
  }
]

index_spl = [
  {
    "status": "success",
    "parameter": {
      "query": "| rest splunk_server=local count=0 /servicesNS/-/-/saved/searches\n| search title=\"Threat - dpz_SCEP_Malware Hit - Rule\"\n| table title search",
      "display": "title,search",
      "context": {
        "guid": "82d407ba-d141-4b36-9c23-99e50cabaae0",
        "artifact_id": 0,
        "parent_action_run": []
      }
    },
    "message": "Total events: 1",
    "data": [
      {
        "search": "index=sec_scep_malware signature!=\"MonitoringTool:Win32/MicTrayDebugger\" file_path!=*RSA* \n| rex field=signature \"(?P<signature_type>\\w+)\\:\" \n| eval trackingvalue=tostring(dest_name)+tostring(file_path)+tostring(detectiontime)\n| dedup trackingvalue \n| eval urgency=if(category==\"Potentially Unwanted Software\",\"low\",urgency)\n| fields _time action dest_name signature_type signature file_path target_process user detection_source urgency category",
        "title": "Threat - dpz_SCEP_Malware Hit - Rule"
      }
    ],
    "summary": {
      "total_events": 1
    }
  }
]

search_spl = tstats_spl[0]['data'][0].get('search')
# print(search_spl)

spl_list = search_spl.split('|')
# print(spl_list)

target_segment = spl_list[1]
# print(target_segment)

spl_addition = "earliest=-6h"
new_spl_segment = target_segment + " " + spl_addition + " "

spl_list[1] = new_spl_segment
# print(spl_list)

new_spl_string = "|".join(spl_list).replace('\n', '')
print(new_spl_string)


search_spl2 = index_spl[0]['data'][0].get('search')
# print(search_spl)

spl_list = search_spl2.split('|')
# print(spl_list)

target_segment = spl_list[0]
# print(target_segment)

spl_addition = "earliest=-6h"
new_spl_segment = target_segment + " " + spl_addition
# print(new_spl_segment)

spl_list[0] = new_spl_segment
# print(spl_list)

new_spl_string = "|".join(spl_list).replace('\n', '')
print(new_spl_string)
