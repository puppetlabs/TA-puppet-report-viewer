
# encoding = utf-8
import json
import requests

def get_certname_facts(certname, server, token):
  # setup the headers
  headers = {'X-Authentication': token}
  #setup the url
  url = "https://%s:8081/pdb/query/v4" % server

  query_string = {}
  query_string["query"] = "facts [name, value] { certname = \"%s\"}" % certname
  
  certname_facts = json.loads(requests.post(url, json=query_string, headers=headers, verify=False).text)

  facts = {}

  for f in certname_facts:
    facts[f['name']] = f['value']

  return facts


def get_resource_events(uuid, server, token):
  # setup the headers
  headers = {'X-Authentication': token}
  #setup the url
  url = "https://%s:8081/pdb/query/v4" % server

  query_string = {}
  query_string["query"] = "reports[hash, status, puppet_version, report_format, catalog_uuid, job_id, cached_catalog_status, configuration_version, environment, corrective_change, noop, noop_pending, certname, transaction_uuid, code_id, resource_events] { transaction_uuid = \"%s\"}" % uuid
  
  resource_events = json.loads(requests.post(url, json=query_string, headers=headers, verify=False).text)

  certname = resource_events[0]['certname']

  #print json.dumps(resource_events, sort_keys=True, indent=2, separators=(',', ': ')

  return resource_events

def submit_to_splunk(forensic_report, splunk, hec):
  # setup the headers
  headers = {"Authorization" : "Splunk %s " % hec }
  #setup the url
  url = "https://%s:8088/services/collector" % splunk

  report = {
    'host': forensic_report['certname'],
    'event': forensic_report
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
    puppet_enterprise_install = helper.get_global_setting("puppet_enterprise_install")
    helper.log_info("puppet_enterprise_install={}".format(puppet_enterprise_install))
    auth_token = helper.get_global_setting("auth_token")
    helper.log_info("auth_token={}".format(auth_token))
    splunk_server = helper.get_global_setting("splunk_server")
    helper.log_info("splunk_server={}".format(splunk_server))
    hec_token = helper.get_global_setting("hec_token")
    helper.log_info("hec_token={}".format(hec_token))

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

    helper.log_info("Alert action generate_puppet_forensic_report started.")
    
    events = helper.get_events()
    for event in events:
        # helper.log_info("event={}".format(event))
        event_dict = event

    event_content = json.loads(event_dict["_raw"])

    transaction_uuid = event_content["transaction_uuid"]

    pdbhostname = helper.get_global_setting("puppet_enterprise_install")
    auth_token = helper.get_global_setting("auth_token")
    splunk_server = helper.get_global_setting("splunk_server")
    hec_token = helper.get_global_setting("hec_token")

    forensic_report = get_resource_events(transaction_uuid, pdbhostname, auth_token)[0]
    certname = forensic_report['certname']
    facts = get_certname_facts(certname, pdbhostname, auth_token)

    forensic_report["facts"] = facts

    #helper.log_info(forensic_report)
    
    submit_to_splunk(forensic_report, splunk_server, hec_token)

    #helper.addevent(json.dumps(forensic_report), sourcetype="puppet:forensic_report")
    helper.writeevents(host="localhost", source="localhost")

    return 0