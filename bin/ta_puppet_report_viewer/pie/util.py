try:
  from urllib.parse import urlparse
except ImportError:
  from urlparse import urlparse

# given a uri return a dict of each PE endpoint behind it
def getendpoints (uri, useproxy=False):
  baseport = None
  if useproxy is True:
    baseport = '443/int_proxy'

  # going to ignore any port values given, force ssl
  hostname = urlparse(uri).hostname
  
  endpoints = {}
  endpoints['rbac'] = 'https://{}:{}/{}'.format(hostname,(baseport or '4433'),'rbac-api/v1')
  endpoints['pdb'] = 'https://{}:{}/{}'.format(hostname,(baseport or '8081'),'pdb/query/v4')
  endpoints['bolt'] = 'https://{}:{}/{}'.format(hostname,(baseport or '8143'),'orchestrator/v1')
  endpoints['console'] = 'https://{}'.format(hostname)
  endpoints['console_hostname'] = hostname

  return endpoints