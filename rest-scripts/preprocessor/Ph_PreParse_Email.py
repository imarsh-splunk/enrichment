import re


def preprocess_container(container):

    new_artifacts = []

    for artifact in container.get('artifacts', []):

        # Create all of the raw Artifacts
        new_artifacts.append(artifact)

        try:
            # Get CEF values from all raw Artifacts
            cef = artifact.get('cef')
            headers = cef.get('emailHeaders')

            fromEmail = re.search(r'<(.*?)>', headers.get('From')).group(1)
            toEmail = re.search(r'<(.*?)>', headers.get('To')).group(1)

            origIp = headers.get('X-Originating-IP')
            if origIp:
                origIp = re.search(r'\[(.*?)\]', origIp).group(1)

                # Create a new "Parsed Artifact(s)" in Container
                new_artifacts.append({
                    'name': 'Parsed Artifact',
                    'source_data_identifier': 'preprocess_container',
                    'cef': {
                        'fromEmail': fromEmail,
                        'toEmail': toEmail,
                        'originatingIp': origIp
                    }
                })

            # Create a new "Parsed Artifact(s)" in Container
            new_artifacts.append({
                'name': 'Parsed Artifact',
                'source_data_identifier': 'preprocess_container',
                'cef': {
                    'fromEmail': fromEmail,
                    'toEmail': toEmail
                }
            })

        except TypeError as e:
            print(e.message)
            # Create new "TypeError when Parsing Artifact!" in Container
            # User will be able to see there was a parsing error in the UI
            new_artifacts.append({
                'name': 'TypeError when Parsing Artifact!',
                'source_data_identifier': 'preprocess_container',
                'cef': {
                    'errorCEF': str(e)
                }
            })

        except AttributeError as e:

            print(e.message)
            # Create new "AttributeError when Parsing Artifact!" in Container
            # User will be able to see there was a parsing error in the UI
            new_artifacts.append({
                'name': 'AttributeError when Parsing Artifact!',
                'source_data_identifier': 'preprocess_container',
                'cef': {
                    'errorCEF': str(e)
                }
            })

    if new_artifacts:
        new_artifacts[-1]['run_automation'] = True

    container['artifacts'] = new_artifacts
    return container