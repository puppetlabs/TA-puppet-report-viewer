
# encoding = utf-8
import json
import requests
from dateutil import parser
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def get_certname_facts(certname, server, token):
  # setup the headers
  headers = {'X-Authentication': token}
  #setup the url
  url = 'https://{}:8081/pdb/query/v4'.format(server)

  facts = {}
  query_string = {}
  query_string['query'] = "facts [name, value] { certname = \"%s\"}" % certname
  
  certname_facts = json.loads(requests.post(url, json=query_string, headers=headers, verify=False).text)

  facts['facts'] = {}

  for f in certname_facts:
    facts['facts'][f['name']] = f['value']

  return facts


def get_resource_events(uuid, server, token):
  
  # setup the headers
  headers = {'X-Authentication': token}
  #setup the url
  url = 'https://{}:8081/pdb/query/v4'.format(server)

  query_string = {}
  query_string['query'] = "reports[hash, status, puppet_version, report_format, catalog_uuid, job_id, cached_catalog_status, configuration_version, environment, corrective_change, noop, noop_pending, certname, transaction_uuid, code_id, resource_events, producer_timestamp, producer, start_time, end_time, receive_time, logs] { transaction_uuid = \"%s\" }" % uuid
  
  resource_events = json.loads(requests.post(url, json=query_string, headers=headers, verify=False).text)

  return resource_events

def submit_to_splunk(detailed_report, splunk, hec):
  # setup the headers
  headers = {"Authorization" : 'Splunk {} '.format(hec) }
  #setup the url
  url = 'https://{}:8088/services/collector'.format(splunk)
  
  # cleanup start_time
  
  ptime = parser.parse(detailed_report['start_time'])
  epoch = ptime.strftime('%s')

  report = {
    'host': detailed_report['certname'],
    'time': epoch,
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
    puppet_db_server = helper.get_global_setting("puppet_db_server")
    helper.log_info("puppet_db_server={}".format(puppet_db_server))
    auth_token = helper.get_global_setting("auth_token")
    helper.log_info("auth_token={}".format(auth_token))
    splunk_server = helper.get_global_setting("splunk_server")
    helper.log_info("splunk_server={}".format(splunk_server))
    splunk_hec_token = helper.get_global_setting("splunk_hec_token")
    helper.log_info("splunk_hec_token={}".format(splunk_hec_token))
    pe_console = helper.get_global_setting("pe_console")
    helper.log_info("pe_console={}".format(pe_console))

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

    #helper.log_info("Alert action generate_detailed_report started.")
    
    events = helper.get_events()
    for event in events:
        event_dict = event

    #helper.log_info(event_dict)

    # attempt to parse the event store to see if it's json
    if is_json(event_dict["_raw"]):
        event_content = json.loads(event_dict["_raw"])
        event_uuid = event_content['transaction_uuid']
        event_puppetdb_callback_hostname = event_content['puppetdb_callback_hostname']
    else:
        event_uuid = None
        event_puppetdb_callback_hostname = ""

    uuid = helper.get_param("transaction_uuid") or event_uuid

    puppetdb_callback_hostname = helper.get_param("puppetdb_callback_hostname") or event_puppetdb_callback_hostname

    #helper.log_info('uuid={}'.format(uuid))

    puppet_db_server = helper.get_global_setting("puppet_db_server")
    auth_token = helper.get_global_setting("auth_token")
    splunk_server = helper.get_global_setting("splunk_server")
    hec_token = helper.get_global_setting("splunk_hec_token")


    pe_console = helper.get_global_setting("pe_console") or puppet_db_server

    resource_response = get_resource_events(uuid, puppet_db_server, auth_token)

    detailed_report = resource_response[0]
    
    certname = detailed_report['certname']
    
    facts= get_certname_facts(certname, puppet_db_server, auth_token)

    detailed_report['facts'] = facts['facts']

    detailed_report['url'] = 'https://{}/#/inspect/report/{}/events'.format(pe_console, detailed_report["hash"])

    detailed_report["puppetdb_callback_hostname"] = puppetdb_callback_hostname

    submit_to_splunk(detailed_report, splunk_server, hec_token)

    helper.writeevents(host="localhost", source="localhost")

    return 0