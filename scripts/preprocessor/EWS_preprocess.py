import re
import traceback


def preprocess_container(container):

    new_artifacts = []

    for artifact in container.get('artifacts', []):

        # Create all of the raw Artifacts
        new_artifacts.append(artifact)

        try: 
            # Get CEF values from all raw Artifacts
            cef = artifact.get('cef')
            bodyHtml = cef.get('bodyHtml')

            if bodyHtml:
                # Parse out fields from bodyHtml as desired
                comp_name = re.search('Reporting Component Name: (.*)<o:p>', bodyHtml).group(1)
                comp_ip = re.search('Reporting Component IP: (.*)<o:p>', bodyHtml).group(1)

                # Create a new "Parsed Artifact(s)" in Container
                new_artifacts.append({
                    'name': 'Parsed Artifact',
                    'source_data_identifier': 'preprocess_container',
                    'cef': {
                        'reportingComponentName': comp_name,
                        'reportingComponentIp': comp_ip
                    }
                })

        except TypeError as e:

            tb = traceback.format_exc()
            # Create new "TypeError when Parsing Artifact!" in Container
            # User will be able to see there was a parsing error in the UI
            new_artifacts.append({
                'name': 'TypeError when Parsing Artifact!',
                'source_data_identifier': 'preprocess_container',
                'cef': {
                    'errorMsg': str(e),
                    'traceBack': str(tb)
                }
            })

        except AttributeError as e:

            tb = traceback.format_exc()
            # Create new "AttributeError when Parsing Artifact!" in Container
            # User will be able to see there was a parsing error in the UI
            new_artifacts.append({
                'name': 'AttributeError when Parsing Artifact!',
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