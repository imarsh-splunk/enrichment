#! /usr/bin/env python
#
# Summary:
#
import requests
from requests.auth import HTTPBasicAuth
import json

def queryEntity(headers, username, password):

	url = "https://falconapi.crowdstrike.com/detects/entities/detects/v2"
	res = '{"ids":["ldt:339bbaf9979c4f1b6d99a618987f33e9:171798940705"],"status": "in_progress"}'
	r = requests.patch(url, headers=headers, auth=HTTPBasicAuth(username, password), data=res)

	if r.status_code != 200:
		print '[-] queryEntity API call failed'
		r.raise_for_status()

	return r.json()

def main():

	username = ''
	password = ''
	headers = {'Content-Type': 'application/json'}

	print queryEntity(headers, username, password)

	
if __name__ == '__main__':
	main()