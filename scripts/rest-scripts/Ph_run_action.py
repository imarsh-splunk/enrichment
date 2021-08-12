import requests
import json

host = '10.0.0.124'
token = 'zQYRKnUNHLoXzBPxDTOWSwVcpWGuOwMYfZARBMlscnw='
headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

post_data = {
  "action": "test connectivity",
  "container_id": 2217,
  "name": "google_dns_test",
  "targets": [
    {
      "assets": [
        "google_dns"
      ],
      "parameters": [
        {
          "domain": "www.splunk.com"
        }
      ],
      "app_id": 14
    }
  ]
}

r = requests.post('https://{}/rest/action_run'.format(host), data=json.dumps(post_data), headers=headers, verify=False)
print(r.json())

ar_id = r.json().get('action_run_id')

r = requests.get('https://{}/rest/action_run/{}?page_size=0'.format(host, ar_id),
                 headers=headers, verify=False).json()

while r.get('status') == 'running':
    r = requests.get('https://{}/rest/action_run/{}?page_size=0'.format(host, ar_id),
                     headers=headers, verify=False).json()
    if r.get('status') == 'success':
        print(json.dumps(r, indent=1))
        break
