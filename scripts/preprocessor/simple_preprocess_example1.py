
suppressed_domains = ['www.proofpoint.com', 'urldefense.com', 'urldefense.proofpoint.com', 'lists.fsisac.com']


def suppress_domain_artifacts(artifacts):
    new_artifacts = []
    for a in artifacts:
        new_artifacts.append(a)
        if a.get('name') and a['name'] != "Domain Artifact" or 'cef' not in a:
            continue

        domain = a['cef'].get('destinationDnsDomain')
        # sanity check
        if not domain:
            a['name'] = "Invalid Domain Artifact"
            continue

        if domain in suppressed_domains:
            a['name'] = "Whitelisted Domain Artifact"
            continue
        
        for candidate in suppressed_domains:
            if domain.endswith(".{}".format(candidate)):
                a['name'] = "Whitelisted Domain Artifact"
                break

    return new_artifacts


# This is the official entry point tha the EWS App will call for each container.
def preprocess_container(container):

    artifacts = container.get('artifacts', [])

    new_artifacts = whitelist_domain_artifacts(artifacts)

    container['artifacts'] = new_artifacts

    return container