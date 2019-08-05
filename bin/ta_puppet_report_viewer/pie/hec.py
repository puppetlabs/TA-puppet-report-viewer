import sys
import json
import requests
from datetime import datetime

# Handle both new and old versions of requests 
try:
  from requests.packages.urllib3.exceptions import InsecureRequestWarning
  requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
except ImportError:
  import urllib3
  urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def post_report(detailed_report, hec_url, hec_token):
  # setup the headers
  headers = {"Authorization" : 'Splunk {} '.format(hec_token) }

  # cleanup start_time
  # start_time = 2019-04-03T12:41:27.481Z
  utc_time = datetime.strptime(detailed_report['start_time'], "%Y-%m-%dT%H:%M:%S.%fZ")
  epoch = (utc_time - datetime(1970, 1, 1)).total_seconds()

  report = {
    'host': detailed_report['certname'],
    'time': epoch,
    'sourcetype': 'puppet:detailed',
    'event': detailed_report
  }

  try:
    requests.post(hec_url, json=report, headers=headers, verify=False)
  except Exception as e:
    raise Exception("HEC Error: {0}".format(e))

def post_action(message, host, hec_url, hec_token):
  # setup the headers
  headers = {"Authorization" : 'Splunk {} '.format(hec_token) }
  
  event = {
    'host': host,
    'sourcetype': 'puppet:action',
    'event': message
  }

  try:
    requests.post(hec_url, json=event, headers=headers, verify=False)
  except Exception as e:
    raise Exception("HEC Error: {0}".format(e))