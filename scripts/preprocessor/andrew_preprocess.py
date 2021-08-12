def preprocess_container(container):
   # Match '[@]' and '[.]' and replace with '@ a' and '.'
   # email_contain = '[@]'
   # dot_contain = '[.]'

   http_contain = 'hxxp'
   http_new = 'http'
   url_prepend = "?"
   
   new_artifacts = []

   for artifact in container.get('artifacts', []):
      cef = artifact.get('cef')
      url = cef.get('requestURL')
      
      if "[@]" in url:
        url = url.replace(http_contain, http_new)
      
      if url and url.lower().startswith(http):
        url = url.replace(url_prepend, '')
        artifact['cef']['requestURL'] = url
      
      new_artifacts.append(artifact)
   
   if new_artifacts:
       new_artifacts[-1]['run_automation'] = True
   
   container['artifacts'] = new_artifacts
   return container