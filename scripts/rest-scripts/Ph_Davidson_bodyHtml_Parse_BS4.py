import bs4



def Add_Email_Body_Artifact(action=None, success=None, container=None, results=None, handle=None,
                            filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('Add_Email_Body_Artifact() called')

    filtered_artifacts_data_1 = phantom.collect2(container=container, datapath=[
        'filtered-data:body_html_filter:condition_1:artifact:*.cef.bodyHtml'])
    filtered_artifacts_item_1_0 = [item[0] for item in filtered_artifacts_data_1]

    Add_Email_Body_Artifact__artifact_id = None

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # <div class="WordSection1">
    # <p class="MsoPlainText">Client IP Address: 192.168.167.148<o:p></o:p></p>
    # <p class="MsoPlainText">Client Hostname: <o:p></o:p></p>
    # <p class="MsoPlainText">Cloud User: scostello<o:p></o:p></p>
    # <p class="MsoPlainText">URL: app.powerbi.com<o:p></o:p></p>
    # <p class="MsoPlainText">URL : <a href="https://app.powerbi.com/PleaseWait">https://app.powerbi.com/PleaseWait</a><o:p></o:p></p>
    # <p class="MsoPlainText">Destination IP: 137.135.16.11<o:p></o:p></p>
    # <p class="MsoPlainText">URL Category: Business<o:p></o:p></p>
    # <p class="MsoPlainText">Reputation: Minimal Risk<o:p></o:p></p>
    # <p class="MsoPlainText">Block Reason: Post Method Block<o:p></o:p></p>
    # <p class="MsoPlainText">Country: US<o:p></o:p></p>
    # <p class="MsoPlainText">Time: [28/Feb/2020:17:19:13 &#43;0000]<o:p></o:p></p>
    # <p class="MsoPlainText">Proxy Server: OCWSG<o:p></o:p></p>
    # <p class="MsoNormal"><o:p>&nbsp;</o:p></p>
    # </div>

    # Write your custom code here...
    bodyHtml = filtered_artifacts_item_1_0[0]

    soup = BeautifulSoup(bodyHtml, 'html.parser')
    # phantom.debug(soup)

    all_classes = soup.findAll("p", {"class": "MsoPlainText"})
    # phantom.debug(str("".join(all_classes)))

    keys = []
    vals = []

    for i in all_classes:
        # phantom.debug(i)
        if i.text and ": " in i.text:
            key = i.text.encode("utf-8").split(": ")[0].replace(" ", "_").replace("URL_", "requestURL").replace("URL",
                                                                                                                "destinationDnsDomain").replace(
                "requestdestinationDnsDomain", "requestURL")
            val = i.text.encode("utf-8").split(": ")[1].strip()
            if val:
                keys.append(key)
                vals.append(val)
        else:
            stripped_text = i.text.strip()
            if stripped_text:
                keys.append("userJustification")
                vals.append(stripped_text)

    artifact_cef_dict = {keys[i]: vals[i] for i in range(len(keys))}
    # phantom.debug(artifact_cef_dict)

    field_mapping = {'Client_IP_Address': ['ip'],
                     'Cloud_User': ['username'],
                     'Destination_IP': ['ip'],
                     'URL': ['domain']}

    # Add "Email Body Artifact" to Phantom Event
    success, message, Add_Email_Body_Artifact__artifact_id = phantom.add_artifact(container=container['id'],
                                                                                  raw_data={},
                                                                                  cef_data=artifact_cef_dict,
                                                                                  label="parsed",
                                                                                  name="Email Body Artifact",
                                                                                  severity="medium",
                                                                                  identifier=None,
                                                                                  artifact_type="site_request",
                                                                                  field_mapping=field_mapping,
                                                                                  trace=False,
                                                                                  run_automation=False)

    phantom.debug(success)
    phantom.debug(message)
    phantom.debug(Add_Email_Body_Artifact__artifact_id)

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key='Add_Email_Body_Artifact:artifact_id',
                          value=json.dumps(Add_Email_Body_Artifact__artifact_id))
    decision_3(container=container)
    filter_4(container=container)

    return