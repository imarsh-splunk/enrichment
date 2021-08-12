import re
import traceback


def preprocess_container(container):

    new_artifacts = []

    for artifact in container.get('artifacts', []):

        # Create all of the raw Artifacts
        new_artifacts.append(artifact)

        # Isolate the original Phishing email from the Submission email
        headers = artifact['cef'].get('emailHeaders')
        if headers:
            auth = headers.get('X-MS-Exchange-Organization-AuthAs')
            if auth == 'Anonymous':

                try:
                    # Retrieve emailHeaders.decodedSubject CEF field
                    cef = artifact.get('cef')
                    decodedSubject = cef['emailHeaders'].get('decodedSubject')

                    # Remove '[External]' subject prefix
                    parsedSubject = decodedSubject.split('[External] ')[1]

                    # Create a new "Parsed Artifact(s)" in Container with parsedSubject CEF
                    new_artifacts.append({
                        'name': 'Parsed Email Artifact',
                        'source_data_identifier': 'preprocess_container',
                        'cef': {
                                'parsedSubject': parsedSubject
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
