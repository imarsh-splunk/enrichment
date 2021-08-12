def risk_score(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('risk_score() called')

    all_ips = phantom.collect2(container=container, datapath=["filtered-data:filter_2:condition_1:multi_collect_1:action_result.data.*.added_data.artifact_ids.*.artifact_id", "filtered-data:filter_2:condition_1:multi_collect_1:action_result.data.*.added_data.all_ips"])
    
    vt_results = phantom.collect2(container=container, datapath=['vt_ip_reputation:action_result.data.*.detected_urls.*.positives', 'vt_ip_reputation:action_result.parameter.ip'], action_results=results)
    
    threatcrowd_results = phantom.collect2(container=container, datapath=['threatcrowd_ip_lookup:action_result.data.*.votes', 'threatcrowd_ip_lookup:action_result.parameter.ip'], action_results=results)
    
    maxmind_results = phantom.collect2(container=container, datapath=['maxmind_geolocate_ips:action_result.data.*.country_iso_code', 'maxmind_geolocate_ips:action_result.parameter.ip'], action_results=results)
    
    qradar_results = phantom.collect2(container=container, datapath=["run_ip_activity_query:action_result.data.*.events.*.sourceip", "run_ip_activity_query:action_result.data.*.events.*.eventcount"])
    
    qradar_results_list = [ip[0] for ip in qradar_results if ip[0] and int(ip[1]) > 0]

    ########## CALCULATE RISK HERE ######################
    #track_ips and associated scored here
    ip_dict = {}
    
    #review vt results looking at number of detecuted_urls positives returned by VT
    for result in vt_results:
        if result[1]:
            if result[0] > 5:
                ip_dict.setdefault(result[1], {})['vt_risk_score'] = 5
            elif result[0] > 1:
                ip_dict.setdefault(result[1], {})['vt_risk_score'] = 2
            else:
                ip_dict.setdefault(result[1], {})['vt_risk_score'] = 0
    
    #review threatcrowd results looking at number "votes" returned by threat crowd - -1 votes means most users said malicious, 0 means equal number and 1 means most say its not malicious
    for result in threatcrowd_results:
        if result[1]:
            if result[0] == -1:
                ip_dict.setdefault(result[1], {})['threatcrowd_risk_score'] = 5
            elif result[0] == 0:
                ip_dict.setdefault(result[1], {})['threatcrowd_risk_score'] = 2
            else:
                ip_dict.setdefault(result[1], {})['threatcrowd_risk_score'] = 0
    
    #review geolocation data - currently only lookin to see if resulting country is in belarus
    for result in maxmind_results:    
        if result[1]:
            if result[0] not in ['US','MX','CA','CN']:
                ip_dict.setdefault(result[1], {})['maxmind_risk_score'] = 10
            else:
                ip_dict.setdefault(result[1], {})['maxmind_risk_score'] = 0
    
    #qradar results risk score calculation - identify those IPs where no results were returned (meaning no activity was found in QRadar 8 to 1 day(s) prior to the offense
    for ip in all_ips:
        if ip[1]:
            if ip[1] not in qradar_results_list:
                ip_dict.setdefault(ip[1], {})['qradar_activity_risk_score'] = 5
            else:
                ip_dict.setdefault(ip[1], {})['qradar_activity_risk_score'] = 0
            
    #calculate total score and add to score tracker
    map(lambda x: ip_dict[x].setdefault('total_risk_score', sum([ip_dict[x][key] for key in ip_dict[x].keys()])), ip_dict.keys())
    
    #print score tracker
    phantom.debug(ip_dict)
    phantom.save_run_data(key="scoring_dict", value=json.dumps(ip_dict, indent=4))
    
    #break ips into high (>=10), medium (>=1) and low risk (0)
    high_risk_ips = [ip for ip in ip_dict.keys() if ip_dict[ip]['total_risk_score'] >= 10]
    med_risk_ips = [ip for ip in ip_dict.keys() if ip_dict[ip]['total_risk_score'] in range(1,10)]
    low_risk_ips = [ip for ip in ip_dict.keys() if ip_dict[ip]['total_risk_score'] == 0]
    
    # collect filtered artifact ids for 'if' condition 1 (low risk)
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        action_results=results,
        conditions=[
            ["filtered-data:filter_1:condition_1:multi_collect_1:action_result.data.*.added_data.all_ips", "in", low_risk_ips],
        ],
        name="risk_score:condition_1")

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        phantom.debug('low severity')
        set_status_add_tag_11(container=container)
        #join_prompt_1(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

    # collect filtered artifact ids for 'if' condition 2 (med risk)
    matched_artifacts_2, matched_results_2 = phantom.condition(
        container=container,
        action_results=results,
        conditions=[
            ["filtered-data:filter_1:condition_1:multi_collect_1:action_result.data.*.added_data.all_ips", "in", med_risk_ips],
        ],
        name="risk_score:condition_2")

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_2 or matched_results_2:
        pin_medium_severity_ips(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_2, filtered_results=matched_results_2)

    # collect filtered artifact ids for 'if' condition 3 (high risk)
    matched_artifacts_3, matched_results_3 = phantom.condition(
        container=container,
        action_results=results,
        conditions=[
            ["filtered-data:filter_1:condition_1:multi_collect_1:action_result.data.*.added_data.all_ips", "in", high_risk_ips],
        ],
        name="risk_score:condition_3")

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_3 or matched_results_3:
        pin_high_severity_ips(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_3, filtered_results=matched_results_3)
    return