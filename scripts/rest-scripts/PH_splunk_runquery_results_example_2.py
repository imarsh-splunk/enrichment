import re

action_results = [
  {
    "status": "success",
    "parameter": {
      "query": "index=\"phantom_app_run\" app_name=VirusTotal asset=9 result_data{}.data{}.resource=\"https://d24nfnljh9ks0g.cloudfront.net/photo/by_id?code=GCZH85ZD6ESS2327R5RV\"\n| rename end_time AS time, result_data{}.data{}.resource AS url, result_data{}.data{}.scan_date AS scan_date, result_data{}.summary.total_scans AS total_scans, result_data{}.summary.positives AS positives\n| eval scan_date = if(isnotnull(scan_date),scan_date,\"Not scanned before\")\n| table time, app_name, container, id, url, scan_date, total_scans, positives, status",
      "command": "search",
      "display": "time, app_name, container, id, url, scan_date, total_scans, positives, status",
      "context": {
        "guid": "baa1f794-58e4-4941-8e8a-bfd98054651e",
        "artifact_id": 0,
        "parent_action_run": []
      }
    },
    "message": "Total events: 0",
    "data": [],
    "summary": {
      "total_events": 0
    }
  },
  {
    "status": "success",
    "parameter": {
      "query": "index=\"phantom_app_run\" app_name=VirusTotal asset=9 result_data{}.data{}.resource=\"http://authentication.decisionresourcesgroup.com/login/Solutions?&tok=YYY2180_pC+Ziwpn7Ce7WbpbQrgUs0qFioszBZglpf72btpoFhSDMEn4dueXFKQQ/gY4MvENbhtwNuDOD3zIxuDhy6buQJC37frCEznhxefsZEIs6fk=\"\n| rename end_time AS time, result_data{}.data{}.resource AS url, result_data{}.data{}.scan_date AS scan_date, result_data{}.summary.total_scans AS total_scans, result_data{}.summary.positives AS positives\n| eval scan_date = if(isnotnull(scan_date),scan_date,\"Not scanned before\")\n| table time, app_name, container, id, url, scan_date, total_scans, positives, status",
      "command": "search",
      "display": "time, app_name, container, id, url, scan_date, total_scans, positives, status",
      "context": {
        "guid": "e41b8f2c-f9f3-458f-ae16-b1bf76e39d53",
        "artifact_id": 0,
        "parent_action_run": []
      }
    },
    "message": "Total events: 2",
    "data": [
      {
        "status": "success",
        "container": "18949",
        "app_name": "VirusTotal",
        "url": [
          "http://authentication.decisionresourcesgroup.com/login/Solutions?&tok=YYY2180_pC+Ziwpn7Ce7WbpbQrgUs0qFioszBZglpf72btpoFhSDMEn4dueXFKQQ/gY4MvENbhtwNuDOD3zIxuDhy6buQJC37frCEznhxefsZEIs6fk=",
          "https://drgdigitalnow.com/view/mail?oeID=fnJc4PNHdTWCsZSsp94M"
        ],
        "scan_date": "Not scanned before",
        "time": "2020-05-29T14:35:55.842000Z",
        "positives": [
          "0",
          "0"
        ],
        "id": "33600",
        "total_scans": [
          "0",
          "0"
        ]
      },
      {
        "status": "success",
        "container": "18949",
        "app_name": "VirusTotal",
        "url": "http://authentication.decisionresourcesgroup.com/login/Solutions?&tok=YYY2180_pC+Ziwpn7Ce7WbpbQrgUs0qFioszBZglpf72btpoFhSDMEn4dueXFKQQ/gY4MvENbhtwNuDOD3zIxuDhy6buQJC37frCEznhxefsZEIs6fk=",
        "scan_date": "Not scanned before",
        "time": "2020-05-21T14:52:47.348000Z",
        "positives": "0",
        "id": "24992",
        "total_scans": "0"
      }
    ],
    "summary": {
      "total_events": 2
    }
  },
  {
    "status": "success",
    "parameter": {
      "query": "index=\"phantom_app_run\" app_name=VirusTotal asset=9 result_data{}.data{}.resource=\"https://drgdigitalnow.com/view/mail?oeID=fnJc4PNHdTWCsZSsp94M\"\n| rename end_time AS time, result_data{}.data{}.resource AS url, result_data{}.data{}.scan_date AS scan_date, result_data{}.summary.total_scans AS total_scans, result_data{}.summary.positives AS positives\n| eval scan_date = if(isnotnull(scan_date),scan_date,\"Not scanned before\")\n| table time, app_name, container, id, url, scan_date, total_scans, positives, status",
      "command": "search",
      "display": "time, app_name, container, id, url, scan_date, total_scans, positives, status",
      "context": {
        "guid": "128b0aa6-f0fd-48f2-a4d3-7cf744e8cad6",
        "artifact_id": 0,
        "parent_action_run": []
      }
    },
    "message": "Total events: 3",
    "data": [
      {
        "status": "success",
        "container": "18949",
        "app_name": "VirusTotal",
        "url": "https://drgdigitalnow.com/view/mail?oeID=fnJc4PNHdTWCsZSsp94M",
        "scan_date": "Not scanned before",
        "time": "2020-05-21T14:59:48.755000Z",
        "positives": "0",
        "id": "25007",
        "total_scans": "0"
      },
      {
        "status": "success",
        "container": "18949",
        "app_name": "VirusTotal",
        "url": [
          "http://authentication.decisionresourcesgroup.com/login/Solutions?&tok=YYY2180_pC+Ziwpn7Ce7WbpbQrgUs0qFioszBZglpf72btpoFhSDMEn4dueXFKQQ/gY4MvENbhtwNuDOD3zIxuDhy6buQJC37frCEznhxefsZEIs6fk=",
          "https://drgdigitalnow.com/view/mail?oeID=fnJc4PNHdTWCsZSsp94M"
        ],
        "scan_date": "Not scanned before",
        "time": "2020-05-29T14:35:55.842000Z",
        "positives": [
          "0",
          "0"
        ],
        "id": "33600",
        "total_scans": [
          "0",
          "0"
        ]
      },
      {
        "status": "success",
        "container": "18949",
        "app_name": "VirusTotal",
        "url": "https://drgdigitalnow.com/view/mail?oeID=fnJc4PNHdTWCsZSsp94M",
        "scan_date": "Not scanned before",
        "time": "2020-05-29T15:06:32.961000Z",
        "positives": "0",
        "id": "33631",
        "total_scans": "0"
      }
    ],
    "summary": {
      "total_events": 3
    }
  },
  {
    "status": "success",
    "parameter": {
      "query": "index=\"phantom_app_run\" app_name=VirusTotal asset=9 result_data{}.data{}.resource=\"https://www.clearslide.com/view/epref?vID=fnJc4PNHdTWCsZSsp94M\"\n| rename end_time AS time, result_data{}.data{}.resource AS url, result_data{}.data{}.scan_date AS scan_date, result_data{}.summary.total_scans AS total_scans, result_data{}.summary.positives AS positives\n| eval scan_date = if(isnotnull(scan_date),scan_date,\"Not scanned before\")\n| table time, app_name, container, id, url, scan_date, total_scans, positives, status",
      "command": "search",
      "display": "time, app_name, container, id, url, scan_date, total_scans, positives, status",
      "context": {
        "guid": "9087ebce-1bd8-48cd-a549-857b12788039",
        "artifact_id": 0,
        "parent_action_run": []
      }
    },
    "message": "Total events: 0",
    "data": [],
    "summary": {
      "total_events": 0
    }
  }
]

# print(action_results)

for i in action_results:
    total_events = i['summary']['total_events']
    if total_events > 0:
        # print(i)
        summary = i['summary']
        query = i['parameter']['query']
        resource = re.search(r'result_data{}.data{}.resource="(.*?)"', query).group(1)
        print(resource)

    total_events = i['summary']['total_events']
    if total_events > 0:
        data = i['data']
        # print(data)
