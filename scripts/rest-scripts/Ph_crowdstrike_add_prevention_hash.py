import requests

data = {
    'client_id': "737a6276579342d29dda4d687097b6c3",
    'client_secret': "NLpzgJOHj3Y0iVt96P4rqxlh5KT8sRCQ7noXk21a"
}

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json'
}

url = "https://api.crowdstrike.com/oauth2/token"

r = requests.post(url, headers=headers, data=data)
# print(r.content)
token = r.json().get('access_token')
# print(token)

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer {}'.format(token)
}

params = [{
                'type': "sha256",
                'value': "eeb27d04c5fb25f7459407c0e5394621f12100e301b22d04a6b8f78e2adbf33c",
                'policy': "detect"
        }]

url = "https://api.crowdstrike.com/indicators/entities/iocs/v1"
r = requests.post(url, headers=headers, json=params)
print(r.content)

