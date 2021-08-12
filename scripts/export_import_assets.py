import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json
from os import path

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Instructions #
########################################################################################################################
# Running the script once will generate asset.json in the directory listed in file_path
# Running the script again against the same directory will pick up the asset.json and import the assets into the target
########################################################################################################################

# CONFIG #
##################################################
ph_from_instance = "https://192.168.180.133"
ph_from_token = ""

ph_to_instance = "https://192.168.180.133"
ph_to_token = ""

file_path = "/Users/dkhorasani/Documents/scripts/"
##################################################

# Script #
rest_params = [
      "action_whitelist",
      "validation",
      "tenants",
      "description",
      "tags",
      "type",
      "primary_voting",
      "product_version",
      "product_name",
      "secondary_voting",
      "configuration",
      "product_vendor",
      "name",
    ]

if not path.exists(file_path + "asset.json"):
    headers = {"ph-auth-token": ph_from_token}
    from_url = ph_from_instance.rstrip('/') + '/rest/asset'
    r = requests.get(from_url, headers=headers, verify=False)
    assets = r.json()
    if assets.get('failed'):
        print "Error in REST call " + str(assets.get('message'))
    new_assets = []
    for asset in assets["data"]:
            new_asset = {}
            for param in rest_params:
                new_asset[param] = asset[param]
            new_assets.append(new_asset)

    with open(file_path + "asset.json", "w+") as f:
        f.write(json.dumps(new_assets))
else:
    headers = {"ph-auth-token": ph_to_token}
    to_url = ph_to_instance.rstrip('/') + '/rest/asset'
    with open(file_path + "asset.json", "r") as f:
        new_assets = json.load(f)
        # print json.dumps(new_assets)
    for config in new_assets:
        # print "Creating asset for: " + config["name"]
        r = requests.post(to_url, headers=headers, verify=False, data=json.dumps(config))
        r_json = r.json()
        success = r_json.get('success')
        if success:
            print "Created asset for product " + config["product_name"] + " with asset name of " + config["name"]
        else:
            err = "\nFAILED with message: " + r_json.get("message") + " for product " + config["product_name"] + " with asset name of " + config["name"]
            print err
            with open(file_path + "errors.txt", "a+") as f:
                f.write(err)
