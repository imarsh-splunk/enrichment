import requests

ep = 'https://api.threatstream.com/api/v1/intelligence/'
apiuser = 'irichardson@splunk.com'
apikey = '09ee2cd9d8a39411b9e1e02590e1b6c966e36208'

params = {
    "datatext": "52.5.29.156",
    "tags": "tag1,tag2",
    "classification": "private",
    "confidence": 49,
    "ip_mapping": True,
    "domain_mapping": False,
    "url_mapping": False,
    "email_mapping": False,
    "md5_mapping": False
}

url = "{}?username={}&api_key={}".format(ep, apiuser, apikey)

r = requests.post(url, data=params)

print(r.content)
