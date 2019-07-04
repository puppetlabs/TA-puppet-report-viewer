# encoding = utf-8

import pie

# alert['global']['puppet_enterprise_console'] = helper.get_global_setting("puppet_enterprise_console")
# alert['global']['puppet_read_user'] = helper.get_global_setting("puppet_read_user")
# alert['global']['puppet_read_user_pass'] = helper.get_global_setting("puppet_read_user_pass")
# alert['global']['splunk_hec_url'] = helper.get_global_setting("splunk_hec_url")
# alert['global']['splunk_hec_token'] = helper.get_global_setting("splunk_hec_token")
# alert['global']['bolt_user'] = helper.get_global_setting("bolt_user")
# alert['global']['bolt_user_pass'] = helper.get_global_setting("bolt_user_pass")
# alert['global']['puppet_bolt_server'] = helper.get_global_setting("puppet_bolt_server")
# alert['global']['puppet_action_hec_token'] = helper.get_global_setting("puppet_action_hec_token")
# alert['global']['puppet_db_url'] = helper.get_global_setting("puppet_db_url")

# alert['param']['transaction_uuid'] = helper.get_param("transaction_uuid")

# events = helper.get_events()
# for event in events:
#     alert['event'] = json.loads(event['_raw'])


def run_bolt_task_investigate(alert):
  # this just writes the alert with a proper task name and param
  # then passes it to the generic run_bolt_task function

  task_name = 'investigate::{}'.format(alert['param']['bolt_investigate_name'])

  # these are the values created by our generic modalert for tasks
  alert['param']['task_name'] = task_name
  alert['param']['task_parameters'] = {}
  alert['param']['bolt_target'] = alert['param']['bolt_investigate_target']
  
  # hardcoding to production for Investigate module
  alert['param']['puppet_environment'] = 'production'

  run_bolt_task(alert)

def run_bolt_task(alert):
  # load our URLs, we generate possible ones assuming the console hostname is valid
  # however if a user provides their own pdb or bolt url it goes here
  # this also allows for us to add an int_proxy feature in the future
  pe_console = alert['global']['puppet_enterprise_console']
  endpoints = pie.util.getendpoints(pe_console)
  rbac_url = endpoints['rbac']
  bolt_url = alert['global']['puppet_bolt_server'] or endpoints['bolt']

  puppet_environment = alert['param']['puppet_environment']

  splunk_hec_url = alert['global']['splunk_hec_url']
  puppet_action_hec_token = alert['global']['puppet_action_hec_token'] or alert['global']['splunk_hec_token']

  bolt_target = alert['param']['bolt_target']
  task_name = alert['param']['task_name']

  message = {
    'message': 'Running task {} on {} '.format(task_name,bolt_target),
    'action_type': 'task',
    'action_name': task_name,
    'action_state': 'starting',
    'alert_event': alert['result'],
  }

  # if this happens to be a puppet run causing this task to be fired
  if alert['result']['transaction_uuid']:
    message['transaction_uuid'] = alert['result']['transaction_uuid']

  pie.hec.post_action(message, bolt_target, splunk_hec_url, puppet_action_hec_token)
  
  bolt_user = alert['global']['bolt_user'] or alert['global']['puppet_read_user']
  bolt_user_pass = alert['global']['bolt_user_pass'] or alert['global']['puppet_read_user_pass']

  auth_token = pie.rbac.genauthtoken(bolt_user,bolt_user_pass,'splunk report viewer',rbac_url)

  job = pie.bolt.reqtask(bolt_target,task_name,auth_token,puppet_environment,bolt_url)

  jobid = job['name']

  jobresults = pie.bolt.getjobresult(jobid, auth_token, bolt_url)

  # right now we're only running tasks against a single target, but may have things in the future returing multiple nodes
  for result in jobresults['items']:
    rmessage = message
    rmessage['action_state'] = result['state']
    rmessage['joburl'] = '{}/#/run/jobs/{}'.format(pe_console,jobid)
    rmessage['result'] = result['result']
    rmessage['transaction_uuid'] = result['transaction_uuid'] or message['transaction_uuid']
    rmessage['start_timestamp'] = result['start_timestamp']
    rmessage['duration'] = result['duration']
    rmessage['finish_timestamp'] = result['finish_timestamp']
    
    if rmessage['action_state'] == 'finished':
      rmessage['message'] = 'Successfully ran task {} on {} '.format(task_name,result['name'])
    elif result['state'] == 'failed':
      rmessage['message'] = 'Failed to run task {} on {} '.format(task_name,result['name'])
    else:
      rmessage['message'] = 'Something happened to task {} on {} that we have no idea about'.format(task_name,result['name'])

    pie.hec.post_action(rmessage, result['name'], splunk_hec_url, puppet_action_hec_token)



# this is our interactive load option
# assumes you're running this library directly from the command line
# cat example_alert.json | python $thisfile.py

if __name__ == "__main__":
  import sys
  import json
  
  alert = json.load(sys.stdin)
  
  run_bolt_task_investigate(alert)