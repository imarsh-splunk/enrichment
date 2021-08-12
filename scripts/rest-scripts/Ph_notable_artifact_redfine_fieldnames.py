import json

action_result = {
        "drilldown_latest_offset": "$info_max_time$",
        "next_steps": "{\"version\":1, \"data\":\"\"}",
        "rule_description": "Sourcefire IPS event(s)",
        "signatures": "OS-OTHER Bash CGI environment variable injection attempt",
        "investigation_profiles": "{}",
        "drilldown_latest": "1564419060.000000000",
        "tag::eventtype": "modaction_result",
        "info_search_time": "1564419062.316254000",
        "orig_action_name": "notable",
        "tag": "modaction_result",
        "indexer_guid": "7EAF4AF4-7392-4442-A0BE-AEEFDE9A996F",
        "owner": "unassigned",
        "rule_title": "MW-006b Medium Sourcefire IPS event from $IDS_Attacks.src$",
        "splunk_server_group": "dmc_group_indexer",
        "status_default": "true",
        "index": "notable",
        "extract_assets": "[\"src\",\"dest\",\"dvc\",\"orig_host\"]",
        "severity": "medium",
        "status_group": "New",
        "event_id": "7EAF4AF4-7392-4442-A0BE-AEEFDE9A996F@@notable@@3d4071abbf91141c5d789b1d403004b8",
        "eventtype": [
          "modnotable_results",
          "nix-all-logs",
          "notable",
          "modnotable_results",
          "nix-all-logs",
          "notable"
        ],
        "linecount": "1",
        "_eventtype_color": "none",
        "late": "07/29/2019 10:37:24",
        "source": "Access - MW-006b Possible medium Sourcefire IPS event - Rule",
        "_bkt": "notable~171~7EAF4AF4-7392-4442-A0BE-AEEFDE9A996F",
        "splunk_server": "dialspindex103",
        "drilldown_name": "Detailed events for MW-006b",
        "drilldown_search": "| datamodel Intrusion_Detection IDS_Attacks search | search sourcetype=cisco:estreamer \"IDS_Attacks.dvc\"=\"SF8140-SCDC1.ad.flydenver.com\" OR \"IDS_Attacks.dvc\"=\"SF8140-SCDC2.ad.flydenver.com\" IDS_Attacks.severity=\"medium\" OR IDS_Attacks.severity=\"low\" IDS_Attacks.src=$IDS_Attacks.src$ IDS_Attacks.dest=10.0.0.0/8 OR IDS_Attacks.dest=172.16.0.0/12 OR IDS_Attacks.dest=192.168.0.0/16",
        "status": "1",
        "count": "1",
        "IDS_Attacks.src": "10.199.46.44",
        "timestamp": "none",
        "orig_sid": "scheduler__splunku_REEtRVNTLU5ldHdvcmtQcm90ZWN0aW9u__RMD5948d4a9f9f91edc3_at_1564419060_96202",
        "owner_realname": "unassigned",
        "search_name": "Access - MW-006b Possible medium Sourcefire IPS event - Rule",
        "orig_rid": "0",
        "early": "07/29/2019 10:37:24",
        "rule_name": "MW-006b Possible medium Sourcefire IPS event",
        "host": "dialspsearch104",
        "_sourcetype": "stash",
        "_indextime": "1564419068",
        "status_end": "false",
        "info_max_time": "1564419060.000000000",
        "info_min_time": "1564332660.000000000",
        "status_description": "Event has not been reviewed.",
        "_cd": "171:111199",
        "sourcetype": "stash",
        "_si": [
          "dialspindex103",
          "notable"
        ],
        "event_hash": "3d4071abbf91141c5d789b1d403004b8",
        "drilldown_earliest": "1564332660.000000000",
        "status_label": "New",
        "security_domain": "access",
        "_time": "2019-07-29T10:51:08.000-06:00",
        "extract_identities": "[\"src_user\",\"user\"]",
        "_raw": "1564419065, search_name=\"Access - MW-006b Possible medium Sourcefire IPS event - Rule\", IDS_Attacks.src=\"10.199.46.44\", count=\"1\", early=\"07/29/2019 10:37:24\", info_max_time=\"1564419060.000000000\", info_min_time=\"1564332660.000000000\", info_search_time=\"1564419062.316254000\", late=\"07/29/2019 10:37:24\", signatures=\"OS-OTHER Bash CGI environment variable injection attempt\"",
        "drilldown_earliest_offset": "$info_min_time$",
        "savedsearch_description": "Sourcefire IPS event(s)",
        "_serial": "0",
        "rule_id": "7EAF4AF4-7392-4442-A0BE-AEEFDE9A996F@@notable@@3d4071abbf91141c5d789b1d403004b8",
        "urgency": "low",
        "priority": "unknown"
      }

for k, v in action_result.iteritems():
    if "." in k or "::" in k:
        # print(k)
        new_key = k.replace('.', '_').replace('::', '_')
        # print(new_key)
        action_result[new_key] = action_result.pop(k)
        # print(action_result[new_key])
# print(action_result)

new_json = json.dumps(action_result, indent=1)
print(new_json)
