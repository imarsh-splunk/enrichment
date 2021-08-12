import tldextract  # Required to extract URL components


campaign_id_use_simple_hash = True  # Make it False to just concatenate FROM and SUBJECT. Make it True to hash them.
campaign_id_digest_body = False  # Make it False to avoid adding hash of bodyHtml


def preprocess_container(container):
    new_artifacts = []
    # campaign_data Dictionary: suspect_sender,report_submitter,campaign_id, attachment_count
    campaign_data = find_campaign_and_global_data(container)

    for artifact in container.get('artifacts', []):
        url_skip_logic(artifact, new_artifacts)                 # 1.2.1 THIS MODIFIES new_artifacts BYREF
        email_role_n_campaign_logic(artifact, campaign_data)    # 1.2.2
        # collect_top_information(artifact, top_info)             # 1.2.3

    # 1.3 Adds global fields to container BYREF based on campaign_data
    set_container_fields(container, campaign_data, new_artifacts)
    
    # 1.4
    addTopArtifacts(new_artifacts, campaign_data)

    container['artifacts'] = new_artifacts

    return container


def url_skip_logic(artifact, new_artifacts):
    if(isWhitelistDomain(artifact) == False):
        new_artifacts.append(artifact)
    else:

        domain = artifact['cef'].get('destinationDnsDomain')
        url = artifact['cef'].get('requestURL')
        skippedURL = ""
        if(domain):
            skippedURL = domain
        elif(url):
            skippedURL = url

        new_artifacts.append({
            'name': 'Whitelist.com Skip Artifact',
            'source_data_identifier': 'preprocess_container',
            'run_automation': False,
            'cef': {
                'skippedURL': skippedURL,
            }
        })

def email_role_n_campaign_logic(artifact, campaign_data):
    if(has_email_headers(artifact)):
        if(is_phish_report(artifact)):
            artifact['cef']['role'] = "REPORT"
        else: #SUSPECT
            artifact['cef']['role'] = "SUSPECT"
            artifact['cef']['campaign_id'] = campaign_data.get("campaign_id")

def collect_top_information(artifact, top_info):
    top_info = {"Content":"TBD"}

# SEARCHES FOR KEY ARTIFACTS IN A CONTAINER TO GET CAMPAIGN DATA
# THIS ALSO ALTERS container variable passed byref.
def find_campaign_and_global_data(container):
    result = {
        'suspect_sender':"TBD SS",
        'report_submitter':"TBD RS",
        'campaign_id':"TBD CID",
        'attachment_count':"TBD HAT"
    }

    suspect_found = False
    report_found = False

    for artifact in container.get('artifacts', []):
        if(has_email_headers(artifact)):
            if(is_phish_report(artifact)):
                report_fields = get_report_fields(artifact)
                result["report_submitter"] = report_fields.get("from_address")
                report_found = True
            else:
                campaign_fields = get_campaign_fields(artifact)
                result["campaign_id"] = campaign_fields.get("campaign_id")
                result["suspect_sender"] = campaign_fields.get("from_address")
                suspect_found = True

        if(suspect_found == True and report_found == True):
            return result
    
    return result

# RECEIVES new_artifacts by reference and adds some TOP entries.
def addTopArtifacts(new_artifacts, campaign_data):
    new_artifacts.append({
        'name': 'TOP_HEADERS',
        'source_data_identifier': 'preprocess_container',
        'run_automation': False,
        'cef': {
                'message': "This will be the placeholder for TOP HEADERS",
                'campaign_id': campaign_data.get("campaign_id")
        }
    })

    new_artifacts.append({
        'name': 'TOP_IOCs',
        'source_data_identifier': 'preprocess_container',
        'run_automation': False,
        'cef': {
                'message': "This will be the placeholder for TOP IOCs",
                'campaign_id': campaign_data.get("campaign_id"),
                'iocs':{'key1':'val1','key2':'val2','url':'verdict'},
                'urls':['url1','url2','url3']
        }
    })

def isWhitelistDomain(artifact):
    destinationDnsDomain = artifact['cef'].get('destinationDnsDomain')
    requestURL = artifact['cef'].get('requestURL')

    if(destinationDnsDomain):
        ext = tldextract.extract(destinationDnsDomain)
        if (ext.domain == "Whitelist" and ext.suffix == "com"):
            return True
    elif (requestURL):
        ext = tldextract.extract(requestURL)
        if (ext.domain == "Whitelist" and ext.suffix == "com"):
            return True
    return False

# Sets Container-level fields (description and custom fields)
def set_container_fields(container, campaign_data, new_artifacts):
    campaign_id = campaign_data.get("campaign_id")
    suspect_sender = campaign_data.get( "suspect_sender")
    report_submitter = campaign_data.get("report_submitter")
    attachment_count = campaign_data.get("attachment_count")

    if (campaign_id!=""):
        container['description'] = "EWS for Exchange - " + campaign_id
        container['custom_fields'] = {
            "Submitter": report_submitter,
            "Sender": suspect_sender,
            "HasAttachments": attachment_count
            }
    else:
        create_debug_artifact("For some reason campaign_id was found false", new_artifacts)

# DETERMINE IF IT IS AN EMAIL ARTIFACT THAT HAS emailHeaders
def has_email_headers(artifact):
    headers = artifact['cef'].get('emailHeaders')
    if headers:
        return True
    else:
        return False

# DETERMINE IF artifact REFERS TO A PHISH REPORT EMAIL 
def is_phish_report(artifact):
    headers = artifact['cef'].get('emailHeaders')
    decoded_subject = headers.get('decodedSubject')
    if decoded_subject.startswith("Potential Phish:"):
        return True
    else:
        return False

def create_debug_artifact(message, new_artifacts):
    new_artifacts.append({
        'name': 'DEBUG',
        'source_data_identifier': 'preprocess_container',
        'run_automation': False,
        'cef': {
                'message': message
        }
    })

def get_campaign_fields(artifact):
    headers = artifact['cef'].get('emailHeaders')
    decoded_subject = headers.get('decodedSubject')
    from_address = headers.get('From')
    campaign_id = ""
    if(campaign_id_use_simple_hash):
        simple_hash = hash("[FROM:" + from_address + "][SUBJECT:" + decoded_subject + "]")
        campaign_id = str(simple_hash)
    else:
        campaign_id = "[FROM:" + from_address + "][SUBJECT:" + decoded_subject + "]"

    if(campaign_id_digest_body):
        body_hash = hash(artifact['cef'].get('bodyHtml'))
        campaign_id += "-" + str(body_hash)

    return {'campaign_id': campaign_id, 'from_address': from_address}

def get_report_fields(artifact):
    headers = artifact['cef'].get('emailHeaders')
    from_address = headers.get('From')
    return {'from_address': from_address}
