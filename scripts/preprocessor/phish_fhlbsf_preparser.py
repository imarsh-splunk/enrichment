from bs4 import UnicodeDammit
# 1. Remove "https://virustotal.com/en/search/query=*" URLS
#     When email is ingested from EWS App, drop VT lookup URLs in email body
# 2. Populate "phish_alarm_analyzer" Custom Event Field with 1 of 3 possible statuses
#     Status comes from a prefix on the Subject of the submission email


# return False to filter the artifact out of the list
def filter_vt_urls(artifact):
    if artifact['name'] == 'URL Artifact':
        if 'virustotal.com' in artifact['cef'].get('requestURL', ''):
            return False
    return True


# This is the official entry point tha the EWS App will call for each container.
def preprocess_container(container):

    artifacts = container.get('artifacts', [])

    if not len(artifacts):
        container['artifacts'] = []

    # remove all VirusTotal URL artifacts
    artifacts = filter(filter_vt_urls, artifacts)

    for artifact in artifacts:
        # submission email artifact
        if artifact.get('cef', {}).get('toEmail') == 'phish@corp.com':
            # extract the subject, convert to unicode
            subject = artifact['cef'].get('emailHeaders', {}).get('Subject')
            subject = UnicodeDammit(subject).unicode_markup

            # "Unlikely a Phish" "Suspicious" and "Likely a Phish"
            if subject.lower().startswith('unlikely a phish:'):
                artifact['cef']['phish_alarm_analyzer'] = 'Unlikely a Phish'

            elif subject.lower().startswith('suspicious:'):
                artifact['cef']['phish_alarm_analyzer'] = 'Suspicious'

            elif subject.lower().startswith('likely a phish:'):
                artifact['cef']['phish_alarm_analyzer'] = 'Likely a Phish'

    container['artifacts'] = artifacts

    return container
