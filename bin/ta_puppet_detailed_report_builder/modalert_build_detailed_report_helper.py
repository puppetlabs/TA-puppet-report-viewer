
# encoding = utf-8
import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def get_certname_facts_reports(certname, receive_time, server, token):
  # setup the headers
  headers = {'X-Authentication': token}
  #setup the url
  url = "https://{}:8081/pdb/query/v4".format(server)

  facts_reports = {}
  query_string = {}
  query_string["query"] = "facts [name, value] { certname = \"%s\"}" % certname
  
  certname_facts = json.loads(requests.post(url, json=query_string, headers=headers, verify=False).text)

  facts_reports['facts'] = {}

  for f in certname_facts:
    facts_reports['facts'][f['name']] = f['value']


  reports_query = {}
  reports_query["query"] = "reports [receive_time, transaction_uuid, corrective_change, noop, noop_pending, hash, status, puppet_version, report_format, catalog_uuid, job_id, cached_catalog_status, configuration_version, environment, code_id, producer_timestamp, producer, start_time, end_time] {certname = \"%s\" and receive_time < \"%s\" order by receive_time desc limit 5}" % (certname, receive_time)

  certname_reports = json.loads(requests.post(url, json=reports_query, headers=headers, verify=False).text)

  facts_reports['reports'] = {}

  for r in certname_reports:
    r_time = r['receive_time']
    facts_reports['reports'][r_time] = r


  return facts_reports


def get_resource_events(uuid, server, token):
  # setup the headers
  headers = {'X-Authentication': token}
  #setup the url
  url = "https://{}:8081/pdb/query/v4".format(server)

  query_string = {}
  query_string["query"] = "reports[hash, status, puppet_version, report_format, catalog_uuid, job_id, cached_catalog_status, configuration_version, environment, corrective_change, noop, noop_pending, certname, transaction_uuid, code_id, resource_events, producer_timestamp, producer, start_time, end_time, receive_time] { transaction_uuid = \"%s\"}" % uuid
  
  resource_events = json.loads(requests.post(url, json=query_string, headers=headers, verify=False).text)

  return resource_events

def submit_to_splunk(detailed_report, splunk, hec):
  # setup the headers
  headers = {"Authorization" : "Splunk {} ".format(hec) }
  #setup the url
  url = "https://{}:8088/services/collector".format(splunk)

  report = {
    'host': detailed_report['certname'],
    'event': detailed_report
  }

  requests.post(url, json=report, headers=headers, verify=False)

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
    hec_token = helper.get_global_setting("hec_token")
    helper.log_info("hec_token={}".format(hec_token))
    pe_console = helper.get_global_setting("pe_console")
    helper.log_info("pe_console={}".format(pe_console))

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

    helper.log_info("Alert action build_detailed_report started.")
    
    events = helper.get_events()
    for event in events:
        # helper.log_info("event={}".format(event))
        event_dict = event

    #helper.log_info(event_dict)

    event_content = json.loads(event_dict["_raw"])

    #helper.log_info(event_content)

    uuid = event_content["transaction_uuid"]

    #helper.log_info(uuid)

    puppet_db_server = helper.get_global_setting("puppet_db_server")
    auth_token = helper.get_global_setting("auth_token")
    splunk_server = helper.get_global_setting("splunk_server")
    hec_token = helper.get_global_setting("hec_token")

    pe_console = helper.get_global_setting("pe_console") or puppet_db_server

    #helper.log_info(uuid)

    detailed_report = get_resource_events(uuid, puppet_db_server, auth_token)[0]
    
    certname = detailed_report['certname']
    receive_time = detailed_report['receive_time']
    
    facts_reports = get_certname_facts_reports(certname, receive_time, puppet_db_server, auth_token)

    detailed_report["facts"] = facts_reports['facts']
    detailed_report["reports"] = facts_reports['reports']

    detailed_report["url"] = 'https://{}/#/inspect/report/{}/events'.format(pe_console, detailed_report["hash"])
    
    # lets remember who generated that original report

    detailed_report["puppetdb_callback_hostname"] = event_content["puppetdb_callback_hostname"]

    submit_to_splunk(detailed_report, splunk_server, hec_token)

    #helper.addevent(json.dumps(forensic_report), sourcetype="puppet:forensic_report")
    helper.writeevents(host="localhost", source="localhost")

    return 0