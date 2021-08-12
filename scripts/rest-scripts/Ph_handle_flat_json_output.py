output = [
  {
    "status": "success",
    "parameter": {
      "context": {
        "guid": "5da679a5-36cd-4af4-8d6b-d31ab40e169e",
        "artifact_id": 0,
        "parent_action_run": []
      }
    },
    "message": "Num sites: 5",
    "data": [
      {
        "siteListingResponse": {
          "siteSummary": [
            {
              "riskscore": "156893.02",
              "id": "22",
              "riskfactor": "1.0",
              "name": "Rapid7 Insight Agents"
            },
            {
              "description": "",
              "riskscore": "74865.945",
              "id": "21",
              "riskfactor": "1.0",
              "name": "Private Cloud - VRA"
            },
            {
              "description": "",
              "riskscore": "27843.16",
              "id": "20",
              "riskfactor": "1.0",
              "name": "On-Prem Server - Active Scan"
            },
            {
              "description": "",
              "riskscore": "0.0",
              "id": "23",
              "riskfactor": "1.0",
              "name": "Azure Test"
            },
            {
              "description": "",
              "riskscore": "0.0",
              "id": "34",
              "riskfactor": "1.0",
              "name": "PhantomTest"
            }
          ],
          "success": "1"
        }
      }
    ],
    "summary": {
      "num_sites": 5
    }
  }
]

sitelist = output[0]['data'][0]['siteListingResponse']['siteSummary']

for s in sitelist:
    sname = s.get('name')
    if sname == "PhantomTest":
        print(s)
