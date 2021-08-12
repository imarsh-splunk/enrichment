import json
import re
import traceback

container_json = '/Users/cblumer/Documents/Ph_Testing_Data/email_container.json'

with open(container_json) as f:
    container = json.load(f)

new_artifacts = []

for artifact in container.get('artifacts', []):

    headers = artifact['cef'].get('emailHeaders')
    if headers:
        auth = headers.get('X-MS-Exchange-Organization-AuthAs')
        if auth == 'Anonymous':

            try:
                # Get CEF values from all raw Artifacts
                cef = artifact.get('cef')
                decodedSubject = cef['emailHeaders'].get('decodedSubject')
                # Parse out original Email Subject
                parsedSubject = decodedSubject.split('[External] ')[1]

                # Create a new "Parsed Artifact(s)" in Container
                new_artifacts.append({
                    'name': 'Parsed Email Artifact',
                    'source_data_identifier': 'EWS_Parser',
                    'cef': {
                        'parsedSubject': parsedSubject
                    }
                })
            except Exception as e:
                print(e)

print(new_artifacts)
