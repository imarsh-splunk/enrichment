import urllib
import traceback
try:
    from urllib.parse import unquote
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
    from urllib import unquote

# Remove proofpoint specifics from the URL
def decode_urls(artifact):

    url_proofpoint = 'https://urldefense.com/v3/__'
    if artifact['name'] == 'URL Artifact':
       if url_proofpoint in artifact['cef']['requestURL']:
            print(artifact['cef']['requestURL'])
            if len(artifact['cef']['requestURL'].split(url_proofpoint)) > 1:
                #print("here1")
                dest_url = artifact['cef']['requestURL'].split(url_proofpoint)[1]
                dest_url = dest_url.replace("]", "")
                encoded = dest_url.replace("[", "")
                decoded = urllib.parse.unquote(encoded)
                parsed_uri = urllib.parse.urlparse(decoded)
                #print(parsed_uri)
                result = '{uri.scheme}://{uri.netloc}{uri.path}'.format(uri=parsed_uri).replace('__', '')
                artifact['cef']['requestURL'] = result
            
    return artifact

def exclude_domains(artifact):
    
    supressed_domains = ['www.proofpoint.com', 'urldefense.com','urldefense.proofpoint.com','lists.fsisac.com']

    if artifact['name'] == 'Domain Artifact':
        if artifact['cef'].get('destinationDnsDomain', '') in supressed_domains:
            return False
    return True

#Begin Process of artifacts within the container
def preprocess_container(container):
    new_artifacts = []
    try:
        artifacts = container.get('artifacts', [])
        #print("Artifacts:")
        #print((artifacts))
        if not len(artifacts):
            container['artifacts'] = []
        
        # Filter excluded Domain Artifacts
        #print("Artifacts:")
        #print(len(artifacts))
        artifacts = list(filter(exclude_domains, artifacts))
        
        # Decode requestURLs containing proofpoint
        #print("Artifacts:")
        #print(len(artifacts))
        #print((artifacts))
        for artifact in artifacts:
            #print((artifact))
            new_artifacts.append(decode_urls(artifact))

        # Add list of Artifacts to 'artifacts' list of dicts
        print("Artifacts:")
        #print((new_artifacts))
        container['artifacts'] = new_artifacts
        
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
    #container['artifacts'] = new_artifacts
    return container

