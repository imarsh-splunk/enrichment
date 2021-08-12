success, message, info = phantom.vault_info(vault_id='8d15164346dfdb75d42a9e40716a5e58b2d5b821', container_id=16)
    
path = info[0]['path']
name = info[0]['name']
fullpath = '{0}/{1}'.format(path, name)
phantom.debug(fullpath)