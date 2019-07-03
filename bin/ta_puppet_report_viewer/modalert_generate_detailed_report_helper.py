# encoding = utf-8
import json
import requests
import collections
from puppet_report_generation import run_report_generation
from datetime import datetime
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def get_resource_events(uuid, server, token):
  
  # setup the headers
  headers = {'X-Authentication': token}
  #setup the url
  url = 'https://{}:8081/pdb/query/v4'.format(server)

  report_elements = [
    'hash', 
    'status', 
    'puppet_version', 
    'report_format', 
    'catalog_uuid', 
    'job_id', 
    'cached_catalog_status', 
    'configuration_version', 
    'environment', 
    'corrective_change', 
    'noop', 
    'noop_pending', 
    'certname', 
    'transaction_uuid', 
    'code_id', 
    'resource_events', 
    'producer_timestamp', 
    'producer', 
    'start_time', 
    'end_time', 
    'receive_time', 
    'logs', 
    'metrics'
  ]

  joined_elements = ', '.join(report_elements)

  query_string = {}
  query_string['query'] = 'reports[{}] {{ transaction_uuid = "{}" }}'.format(joined_elements, uuid)
  
  resource_events = json.loads(requests.post(url, json=query_string, headers=headers, verify=False).text)

  return resource_events

def submit_to_splunk(detailed_report, splunk, hec):
  # setup the headers
  headers = {"Authorization" : 'Splunk {} '.format(hec) }
  #setup the url
  url = 'https://{}:8088/services/collector'.format(splunk)
  
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

  requests.post(url, json=report, headers=headers, verify=False)

def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        return False
    return True

def process_event(helper, *args, **kwargs):
    """
    # IMPORTANT
    # Do not remove the anchor macro:start and macro:end lines.
    # These lines are used to generate sample code. If they are
    # removed, the sample code will not be updated when configurations
    # are updated.

    [sample_code_macro:start]

    # The following example gets the setup parameters and prints them to the log
    puppet_enterprise_console = helper.get_global_setting("puppet_enterprise_console")
    helper.log_info("puppet_enterprise_console={}".format(puppet_enterprise_console))
    puppet_read_user = helper.get_global_setting("puppet_read_user")
    helper.log_info("puppet_read_user={}".format(puppet_read_user))
    puppet_read_user_pass = helper.get_global_setting("puppet_read_user_pass")
    helper.log_info("puppet_read_user_pass={}".format(puppet_read_user_pass))
    splunk_hec_url = helper.get_global_setting("splunk_hec_url")
    helper.log_info("splunk_hec_url={}".format(splunk_hec_url))
    splunk_hec_token = helper.get_global_setting("splunk_hec_token")
    helper.log_info("splunk_hec_token={}".format(splunk_hec_token))
    bolt_user = helper.get_global_setting("bolt_user")
    helper.log_info("bolt_user={}".format(bolt_user))
    bolt_user_pass = helper.get_global_setting("bolt_user_pass")
    helper.log_info("bolt_user_pass={}".format(bolt_user_pass))
    puppet_bolt_server = helper.get_global_setting("puppet_bolt_server")
    helper.log_info("puppet_bolt_server={}".format(puppet_bolt_server))
    puppet_action_hec_token = helper.get_global_setting("puppet_action_hec_token")
    helper.log_info("puppet_action_hec_token={}".format(puppet_action_hec_token))
    puppet_db_url = helper.get_global_setting("puppet_db_url")
    helper.log_info("puppet_db_url={}".format(puppet_db_url))

    # The following example gets the alert action parameters and prints them to the log
    transaction_uuid = helper.get_param("transaction_uuid")
    helper.log_info("transaction_uuid={}".format(transaction_uuid))


    # The following example adds two sample events ("hello", "world")
    # and writes them to Splunk
    # NOTE: Call helper.writeevents() only once after all events
    # have been added
    helper.addevent("hello", sourcetype="sample_sourcetype")
    helper.addevent("world", sourcetype="sample_sourcetype")
    helper.writeevents(index="summary", host="localhost", source="localhost")

    # The following example gets the events that trigger the alert
    events = helper.get_events()
    for event in events:
        helper.log_info("event={}".format(event))

    # helper.settings is a dict that includes environment configuration
    # Example usage: helper.settings["server_uri"]
    helper.log_info("server_uri={}".format(helper.settings["server_uri"]))
    [sample_code_macro:end]
    """

    # Lets generate that dict we need

    alert = {}
    alert['global'] = {}
    alert['param'] = {}

    alert['global']['puppet_enterprise_console'] = helper.get_global_setting("puppet_enterprise_console")
    alert['global']['puppet_read_user'] = helper.get_global_setting("puppet_read_user")
    alert['global']['puppet_read_user_pass'] = helper.get_global_setting("puppet_read_user_pass")
    alert['global']['splunk_hec_url'] = helper.get_global_setting("splunk_hec_url")
    alert['global']['splunk_hec_token'] = helper.get_global_setting("splunk_hec_token")
    alert['global']['bolt_user'] = helper.get_global_setting("bolt_user")
    alert['global']['bolt_user_pass'] = helper.get_global_setting("bolt_user_pass")
    alert['global']['puppet_bolt_server'] = helper.get_global_setting("puppet_bolt_server")
    alert['global']['puppet_action_hec_token'] = helper.get_global_setting("puppet_action_hec_token")
    alert['global']['puppet_db_url'] = helper.get_global_setting("puppet_db_url")

    alert['param']['transaction_uuid'] = helper.get_param("transaction_uuid")

    events = helper.get_events()
    for event in events:
        alert['result'] = json.loads(event)
    
    run_report_generation(alert)



    #helper.log_info(event_dict)

    # attempt to parse the event store to see if it's json
    if is_json(event_dict["_raw"]):
        event_content = json.loads(event_dict["_raw"])
        event_uuid = event_content['transaction_uuid']
        event_pe_console = event_content['pe_console']
    else:
        event_uuid = None
        event_pe_console = ""

    uuid = helper.get_param("transaction_uuid") or event_uuid

    pe_console = helper.get_param("pe_console") or event_pe_console

    #helper.log_info('uuid={}'.format(uuid))

    puppet_db_server = helper.get_global_setting("puppet_db_server")
    auth_token = helper.get_global_setting("auth_token")
    splunk_server = helper.get_global_setting("splunk_server")
    hec_token = helper.get_global_setting("splunk_hec_token")

    
    
    
    
    
    
    
    resource_response = get_resource_events(uuid, puppet_db_server, auth_token)

    detailed_report = resource_response[0]

    mdict = collections.defaultdict(dict)

    for m in detailed_report['metrics']['data']:
      mdict[m['category']][m['name']] = m['value']
    
    detailed_report['metrics'] = dict(mdict)

    detailed_report['url'] = 'https://{}/#/inspect/report/{}/events'.format(pe_console, detailed_report["hash"])

    detailed_report["pe_console"] = pe_console

    submit_to_splunk(detailed_report, splunk_server, hec_token)

    helper.writeevents(host="localhost", source="localhost")

    return 0