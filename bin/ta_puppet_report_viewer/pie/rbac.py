import sys
import json
import requests

# Handle both new and old versions of requests 
try:
  from requests.packages.urllib3.exceptions import InsecureRequestWarning
  requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
except ImportError:
  import urllib3
  urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def genauthtoken(username, password, label, url):
  req = {
    'login': username,
    'password': password,
    'lifetime': '0',
    'label': label,
  }

  endpoint = '{}/auth/token'.format(url)

  #https://puppet.angrydome.org:4433/rbac-api/v1/auth/token
  try:
    r = requests.post(endpoint, json=req, verify=False)
  except:
    print('Unexpected error:', sys.exc_info()[0])
    raise
  
  if r.status_code == 200:
    token = json.loads(r.text)['token']
    return token
  else:
    raise ValueError('Unable to get PE auth token', r.status_code, r.text)