#/usr/bin/env python

import json

alert = {}

alert = {}
alert['global'] = {}
alert['param'] = {}

alert['global']['puppet_enterprise_console'] = 'https://puppet.angrydome.org'
alert['global']['puppet_read_user'] = 'splunk'

alert['global']['puppet_read_user_pass'] = 'puppetlabs'

alert['global']['splunk_hec_url'] = 'https://splunk.angrydome.org:8088/services/collector'
alert['global']['splunk_hec_token'] = 'fdc081b8-feb7-4e1b-97cc-6a8d141b7cd0'
alert['global']['bolt_user'] = 'splunkrunner'
alert['global']['bolt_user_pass'] = 'puppetlabs'
alert['global']['puppet_bolt_server'] = 'https://puppet.angrydome.org:8143/orchestrator/v1'
alert['global']['puppet_action_hec_token'] = '7b2802a3-d11d-4a75-8ded-fa1acd1fbed6'
alert['global']['puppet_db_url'] = 'https://puppet.angrydome.org:8081/pdb/query/v4'

alert['param']['transaction_uuid'] = '6b6ae8ad-fe34-4b34-9f64-9bd00eeb5d4b'
alert['param']['bolt_investigate_name'] = 'lastlogin'
alert['param']['bolt_investigate_target'] = 'web-front-ends-4nh1.c.splunk-217321.internal'



result_json = open('result.json')
results = json.load(result_json)
result_json.close

alert['result'] = results['result']

with open('debugalert.json', 'w') as outfile:  
    json.dump(alert, outfile,indent=2, separators=(',', ': '), sort_keys=True)