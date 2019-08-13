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

#https://puppet.angrydome.org:8143/orchestrator/v1/command/task
def post(endpoint, req, headers):

  try:
    r = requests.post(endpoint, json=req, headers=headers, verify=False)
  except:
    print('Unexpected error:', sys.exc_info()[0])
    raise

  if r.status_code != 202:
    raise ValueError('Unable to submit task command', r.status_code, r.text)

  return json.loads(r.text)['job']

def reqtask(node, task, token, environment, url, parameters=None):
  headers = {'X-Authentication': token}
  params = {}
  if parameters:
    params = json.loads(parameters)
  
  req = {
    'environment' : environment,
    'task' : task,
    'params' : params,
    'scope' : {
      'nodes' : [node]
    }
  }

  return post('{}/command/task'.format(url), req, headers)

def reqdeploy(node, noop, token, environment, url):
  headers = {'X-Authentication': token}

  req = {
    'environment' : environment,
    'noop' : noop,
    'scope' : {
      'nodes' : [node]
    }
  }

  return post('{}/command/deploy'.format(url), req, headers)



# Get job state
# given a joburl and token, return state
def getjobstate(joburl, token):
  headers = {'X-Authentication': token}
  try:
    r = requests.get(joburl, headers=headers, verify=False)
  except:
    print('Unexpected error:', sys.exc_info()[0])
    raise
 
  if r.status_code != 200:
    raise ValueError('Unable to get job status endpoints:', joburl, r.status_code, r.text)
  
  return json.loads(r.text)['state']


# Get a Job Result
# Given a job id, loop over getjobstate() until complete
# or timeout is exceeded
def getjobresult(job, token, url, wait=10, timeout=360):
  joburl = '{}/jobs/{}'.format(url,job)
  task_timeout = int(timeout)
  runtime = 0
  completed = ['stopped', 'finished', 'failed']
  while runtime < task_timeout:
    if getjobstate(joburl, token) in completed:
      result = getjobreport(job, token, url)
      return result

    time.sleep(wait)
    runtime += wait

  # we should only get here because of timeout
  raise ValueError('Timeout execeeded waiting for: {} timeout: {} seconds'.format(joburl, timeout))

# Get Job Report
# This includes the full run details and the metadata / results of any task written
# pseudo private method of getjobresult
def getjobreport(job, token, url):
  headers = {'X-Authentication': token}
  reporturl = '{}/jobs/{}/nodes'.format(url,job)

  #https://puppet.angrydome.org:8143/orchestrator/v1/jobs/jobidnumber/nodes
  try:
    r = requests.get(reporturl, headers=headers, verify=False)
  except:
    print('Unexpected error:', sys.exc_info()[0])
    raise

  if r.status_code == 200:
    report = json.loads(r.text)
    return report

  raise ValueError('Unable to get job status for job name:', job, r.status_code, r.text)
