import re
import traceback
import sys
import urllib
import urlparse


def preprocess_container(container):

	new_artifacts = []

	raw_email = container['data'].get('raw_email')

	new_artifacts.append({
                            'name': 'Raw Email Artifact',
                            'source_data_identifier': 'preprocess_container',
                            'cef': {
                                'rawEmailOutput': raw_email
                            }
                        }) 

	for artifact in container.get('artifacts', []):
    	# Create all of the raw Artifacts
		new_artifacts.append(artifact)

	container['artifacts'] = new_artifacts
	return container
