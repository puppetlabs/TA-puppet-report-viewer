import json
import sys
import requests
import time

# Handle both new and old versions of requests 
try:
  from requests.packages.urllib3.exceptions import InsecureRequestWarning
  requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
except ImportError:
  import urllib3
  urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# https://puppet.angrydome.org:8081/pdb/query/v4
def getpuppetreport(uuid, url, token):
  query_string = {}
  query_string['query'] = 'reports[] {{ transaction_uuid = "{}" }}'.format(uuid)
  
  try:
    r = requests.post(url, json=query_string, headers={'X-Authentication': token}, verify=False)
  except:
    print('Unexpected error:', sys.exc_info()[0])
    raise
  
  if r.status_code != 200:
    raise ValueError('Unable to get report for transaction uuid:', uuid, r.status_code, r.text)

  return json.loads(r.text)

# https://puppet.angrydome.org:8081/pdb/query/v4
def query(pql, url, token):
  try:
    r = requests.post(url, json=pql, headers={'X-Authentication': token}, verify=False)
  except:
    print('Unexpected error:', sys.exc_info()[0])
    raise
  
  if r.status_code != 200:
    raise ValueError('Unable run query:', pql, r.status_code, r.text)

  return json.loads(r.text)
