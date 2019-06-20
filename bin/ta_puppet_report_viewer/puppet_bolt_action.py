
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


def run_bolt_task(alertdata):

    # parse puppet_enterprise_console and define URI

    # set pe_console value

    # check if puppet_db_url also exists, that overrides pe_console for accessing puppetdb

    # pie.rbac.genauthtoken using the right url

    # parse params from event data (transactuuid, etc)

    # notify splunk hec with action that performing lookup of report for transactionuuid
    # pie.hec.submit()

    # pie.pdb.getpuppetreport with array of fields to use

    # optionally get facts

    # generate final detailed report dict

    # pie.hec.submit() with report dict, hec token, url

    # if error, parse / handle error / submit data to action end point



    print('foo')