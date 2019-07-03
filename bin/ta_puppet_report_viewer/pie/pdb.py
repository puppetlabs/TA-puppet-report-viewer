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

def getpuppetreport(uuid, url, token):
  
  # setup the headers
  headers = {'X-Authentication': token}

  # https://puppet.angrydome.org:8081/pdb/query/v4

  query_string = {}
  query_string['query'] = 'reports[] {{ transaction_uuid = "{}" }}'.format(uuid)
  
  try:
    r = requests.post(url, json=query_string, headers=headers, verify=False)
  except:
    print('Unexpected error:', sys.exc_info()[0])
    raise
  
  if r.status_code == 200:
    report = json.loads(r.text)
    return report
  else:
    raise ValueError('Unable to get report for transaction uuid:', uuid, r.status_code, r.text)
  
def query(pql, url, token):
  # setup the headers
  headers = {'X-Authentication': token}

  # https://puppet.angrydome.org:8081/pdb/query/v4

  try:
    r = requests.post(url, json=pql, headers=headers, verify=False)
  except:
    print('Unexpected error:', sys.exc_info()[0])
    raise
  
  if r.status_code == 200:
    report = json.loads(r.text)
    return report
  else:
    raise ValueError('Unable run query:', pql, r.status_code, r.text)