import re

run_query_results = [
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

#         "search": "| tstats count min(_time) as firstTime max(_time) as lastTime from datamodel=Network_Resolution where DNS.message_type=response AND DNS.record_type=TXT by DNS.src DNS.dest DNS.answer DNS.record_type \n| `drop_dm_object_name(\"DNS\")` \n| eval anslen=len(answer) \n| where anslen>100 \n| `ctime(firstTime)` \n| `ctime(lastTime)` \n| fields src dest answer anslen record_type firstTime lastTime count",

spl = run_query_results[0]['data'][0].get('search')
# phantom.debug(spl)

earliest = 1589414100.000000000
latest = 1589415000.000000000

spl_list = spl.split('|')
# phantom.debug(spl_list)

if 'tstats' and 'by' in spl_list[1]:

  target = spl_list[1].split('by')[0]
  remaining = spl_list[1].split('by')[1]
  spl_addition = "earliest={} latest={}".format(earliest, latest)
  new_spl_segment = target + " " + spl_addition + " " + "by" + remaining
  spl_list[1] = new_spl_segment

  rewrite_SPL__rewritten_spl = "|".join(spl_list).replace('\n', '')
  print(rewrite_SPL__rewritten_spl)

elif 'tstats' in spl_list[1] and 'by' not in spl_list[1]:

  spl_addition = "earliest={} latest={}".format(earliest, latest)
  new_spl_segment = spl_list[1] + " " + spl_addition + " "
  spl_list[1] = new_spl_segment

  rewrite_SPL__rewritten_spl = "|".join(spl_list).replace('\n', '')
  print(rewrite_SPL__rewritten_spl)

else:
  spl_addition = "earliest={}".format(earliest)

  new_spl_segment = spl_list[0] + " " + spl_addition + " "

  spl_list[0] = new_spl_segment

  rewrite_SPL__rewritten_spl = "|".join(spl_list).replace('\n', '')
  # phantom.debug(rewrite_SPL__rewritten_spl)
