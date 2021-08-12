# return False to filter the artifact out of the list
def exclude_domains(artifact):

    supressed_domains = ['www.virustotal.com', 'gsk.com', 'GSK.COM', 'urldefense.com', 'www.microsoft.com', 
    'support.office.com', 'admin.microsoft.com', 'forms.office.com', 'go.microsoft.com', 'click.email.office.com',
    'view.email.office.com', 'image.email.office.com', 'www.office.com', 'techcommunity.microsoft.com',
    'docs.microsoft.com', 'cloudblogs.microsoft.com', 'www.w3.org', 'schemas.microsoft.com']

    if artifact['name'] == 'Domain Artifact':
        if artifact['cef'].get('destinationDnsDomain', '') in supressed_domains:
            return False
    return True

# This is the official entry point tha the EWS App will call for each container.
def preprocess_container(container):

    artifacts = container.get('artifacts', [])

    if not len(artifacts):
        container['artifacts'] = []

    # Filter excluded URL Artifacts
    # artifacts = filter(exclude_urls, artifacts)

    # Filter excluded Domain Artifacts
    artifacts = filter(exclude_domains, artifacts)

    # Add list of Artifacts to 'artifacts' list of dicts
    # container['artifacts'] = artifacts

    return container
