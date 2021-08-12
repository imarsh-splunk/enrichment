 import re
import traceback
import sys
import urllib
import urlparse


def preprocess_container(container):
    new_artifacts = []

    for artifact in container.get('artifacts', []):

        # Create all of the raw Artifacts
        new_artifacts.append(artifact)

        bodytxt = artifact['cef'].get('bodyText')
        if bodytxt:
            
            try:
                msgid = re.search(r'Message-ID: (.*?)\n', bodytxt).group(1)
                xmailer = re.search(r'X-Mailer: (.*?)\n', bodytxt).group(1)
                rpath = re.search(r'Return-Path: (.*?)\n', bodytxt).group(1)
                reporter = re.search(r'Reporting User: (.*?)\n', bodytxt).group(1)
                auth = re.search(r'X-MS-Exchange-Organization-AuthAs: (.*?)\n', bodytxt).group(1)
                subject = re.search(r'Subject: (.*?)\n', bodytxt).group(1)
                
                if "[External] " in subject:
                    parsedSubject = subject.split('[External] ')[1]

                    # Create a new "Parsed Artifact(s)" in Container with parsedSubject CEF
                        new_artifacts.append({
                            'name': 'Suspected Phish Email Artifact',
                            'source_data_identifier': 'preprocess_container',
                            'cef': {
                                'exchangeAuthOrgAs': auth,
                                'parsedSubject': parsedSubject,
                                'exchangeMsgId': msgid,
                                'xMailer': xmailer,
                                'returnPathSender': rpath,
                                'reportingUser': reporter
                            }
                        })
            except Exception as e:

                    tb = traceback.format_exc()
                    # Create new "TypeError when Parsing Artifact!" in Container
                    # User will be able to see there was a parsing error in the UI
                    new_artifacts.append({
                        'name': 'Exception when parsing Email Artifact!',
                        'source_data_identifier': 'preprocess_container',
                        'cef': {
                            'errorMsg': str(e),
                            'traceBack': str(tb)
                        }
                    })

        # Isolate the original Phishing email from the Submission email
        headers = artifact['cef'].get('emailHeaders')
        if headers:
            auth = headers.get('X-MS-Exchange-Organization-AuthAs')
            auth_options = {'Anonymous', 'Internal'}
            if auth in auth_options:

                try:
                    # Retrieve emailHeaders.decodedSubject CEF field
                    cef = artifact.get('cef')
                    decodedSubject = cef['emailHeaders'].get('decodedSubject')

                    # Remove '[External]' subject prefix
                    # remove newlines if present in subject
                    # strip white spaces on beginning and end if present
                    # If '[External]' is not present within the email subject, then pass original
                    if '[External]' in decodedSubject:
                        parsedSubject = decodedSubject.split('[External] ')[1].replace("\r\n", "").strip()

                        # Create a new "Parsed Artifact(s)" in Container with parsedSubject CEF
                        new_artifacts.append({
                            'name': 'Parsed Email Artifact',
                            'source_data_identifier': 'preprocess_container',
                            'cef': {
                                'exchangeAuthOrgAs': auth,
                                'parsedSubject': parsedSubject
                            }
                        })
                    else:

                        new_artifacts.append({
                            'name': 'Parsed Email Artifact',
                            'source_data_identifier': 'preprocess_container',
                            'cef': {
                                'exchangeAuthOrgAs': auth,
                                'parsedSubject': decodedSubject
                            }
                        })

                except Exception as e:

                    tb = traceback.format_exc()
                    # Create new "TypeError when Parsing Artifact!" in Container
                    # User will be able to see there was a parsing error in the UI
                    new_artifacts.append({
                        'name': 'Exception when parsing Email Artifact!',
                        'source_data_identifier': 'preprocess_container',
                        'cef': {
                            'errorMsg': str(e),
                            'traceBack': str(tb)
                        }
                    })

        url = artifact['cef'].get('requestURL')
        if url and "https://urldefense.proofpoint.com" in url:
            try:
                query = urlparse.urlparse(url).query
                param = urlparse.parse_qs(query)
                u = (param['u'][0].replace('-', '%').replace('_', '/'))
                parsedURL = urllib.unquote(u)

                # Create a new "Parsed Artifact(s)" in Container with parsedSubject CEF
                new_artifacts.append({
                    'name': 'Parsed URL Artifact',
                    'source_data_identifier': 'preprocess_container',
                    'cef': {
                        'requestURL': parsedURL
                    }
                })

            except Exception as e:

                tb = traceback.format_exc()
                # Create new "TypeError when Parsing Artifact!" in Container
                # User will be able to see there was a parsing error in the UI
                new_artifacts.append({
                    'name': 'Exception when parsing URL Artifact!',
                    'source_data_identifier': 'preprocess_container',
                    'cef': {
                        'errorMsg': str(e),
                        'traceBack': str(tb)
                    }
                })

        domain = artifact['cef'].get('destinationDnsDomain')

        whitelist_domains = {'www.w3.org',
                             'crowdstrike.com',
                             'schemas.microsoft.com',
                             'urldefense.proofpoint.com'}

        if domain and domain not in whitelist_domains:
            try:
                # Create a new "Parsed Artifact(s)" in Container with parsedSubject CEF
                new_artifacts.append({
                    'name': 'Parsed Domain Artifact',
                    'source_data_identifier': 'preprocess_container',
                    'cef': {
                        'destinationDnsDomain': domain
                    }
                })

            except Exception as e:

                tb = traceback.format_exc()
                # Create new "TypeError when Parsing Artifact!" in Container
                # User will be able to see there was a parsing error in the UI
                new_artifacts.append({
                    'name': 'Exception when parsing Domain Artifact!',
                    'source_data_identifier': 'preprocess_container',
                    'cef': {
                        'errorMsg': str(e),
                        'traceBack': str(tb)
                    }
                })

    if new_artifacts:
        new_artifacts[-1]['run_automation'] = True

    container['artifacts'] = new_artifacts
    return container
