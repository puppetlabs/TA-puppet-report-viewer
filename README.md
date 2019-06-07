Puppet Report Viewer
==============

Description
-----------
This is a Splunk Addon that provides views into the status of the Puppet installation that is sending its reports to Splunk via the HEC. To use this viewer it has to be installed alongside the `splunk_hec` report processor provided in the [Puppet Forge](https://forge.puppet.com/puppetlabs/splunk_hec). The report processor sends data from Puppet to Splunk via the [HTTP Event Collector](https://docs.splunk.com/Documentation/Splunk/latest/Data/UsetheHTTPEventCollector).

The steps to get this addon working are:

1. Install the Puppet Report Viewer addon
2. Create atleast one HEC input (puppet:summary)
3. Install `splunk_hec` module in Puppet environment and configure with the HEC token and Splunk Server

Once configured, the overview page will start showing Puppet run report status, and information about changes over various windows of time. The views can be customized, updated, modified to suit your needs.

![Reports Overview](https://raw.githubusercontent.com/puppetlabs/TA-puppet-report-viewer/master/README/img/overview.png)

For detailed report generation, a feature for Puppet Enterprise Users, there are additional steps one can perform, that first require configuration the AddOn with the appropriate credentials to talk to PuppetDB and to submit events to Splunk:

1. Create puppet:detailed HEC input
2. Create a Splunk [user and role](https://puppet.com/docs/pe/latest/rbac_user_roles_intro.html#create-a-new-user-role) in the Puppet Enterprise console, with the permission to "View node data from PuppetDB" under the Nodes Type
3. Configure Puppet Enterprise to support long life [authentication tokens](https://puppet.com/docs/pe/latest/rbac_token_auth_intro.html#change-the-token-s-default-lifetime)
4. Generate an authentication token (example command) : `curl -k -X POST -H 'Content-Type: application/json' 
 -d '{"login": "splunk", "password": "password", "lifetime": "1y"}' https://localhost:4433/rbac-api/v1/auth/token`
5. On the configuration page of the addon provide the hostname of the PuppetDB server & auth token, along with the hostname of the Splunk instace running the HEC along with the puppet:detailed HEC token (this is important to use the puppet:detailed token and sourcetype, otherwise it is possible to create an alert action that continually calls itself)
6. With the addon configured, perform a search for a specific event (such as a puppet run with a failed or changed status) `sourcetype="puppet:summary"| spath status | search status=failed` save it as an alert, and assign the action "Generate detailed report" from the action menu. No configuration of the action is needed.

![Addon Configuration Screen](https://raw.githubusercontent.com/puppetlabs/TA-puppet-report-viewer/master/README/img/configuration.png)

![Report Builder](https://raw.githubusercontent.com/puppetlabs/TA-puppet-report-viewer/master/README/img/report_builder.png)

Advanced Configuration
----------------
All report views support using custom indexes for storing event data. They accomplish this with a series of advanced search macros. The queries assume each sourcetype can be stored in it's own index (facts, summary reports, detailed reports, bolt events, action events, Puppet Enterprise metrics).

There is one top level macro, `puppet_index` which defaults to "", if you configure the HEC to use a different index and want all Puppet in that index, change that value here to be `index=puppetindexname`.

If you are using [puppetlabs/splunk_hec](https://forge.puppet.com/puppetlabs/splunk_hec/readme) version 0.5.0 or later, you can specify different HEC tokens for Summary Reports, Facts, and Metrics. Then create an index and an associated HEC token associated with those sourcetypes, and configure both the splunk_hec module in Puppet with those new values. Actions, Bolt Events, and Detailed Reports are all submitted via different tools and would need ot be changed according to use a different HEC token. Then the corresponding macro's updated to use those indexes.

For example, if you want most Puppet data to go to one index, but Facts, Metrics, and Detailed Reports to go to their own indexes, one would follow these steps:
- Create four indexes: puppet_data, puppet_facts_data, puppet_metrics_data, and puppet_detailed_data (or whatever name makes sense), each with their desired timespan, retention, etc.
- Create four HEC's (example names):
1. `puppet` with sourcetype of `puppet:summary` and the index `puppet_data`
2. `puppet_facts` with sourcetype of `puppet:facts` and the index of `puppet_facts_data`
3. `puppet_metrics` with sourcetype of `puppet:metrics` and the index of `puppet_metrics_data`
4. `puppet_detailed` with sourcetype of `puppet:detailed` and the index of `puppet_detailed_data`
- Configure the `splunk_hec` module with the corresponding tokens
1. `splunk_hec::token` with the value from the `puppet` HEC (since you want all Puppet using splunk_hec plugin to go here, except for facts and metrics)
2. `splunk_hec::token_facts` with the value from the `puppet_facts` HEC
3. `splunk_hec::token_metrics` with the value from the `puppet_metrics` HEC
- Update the Puppet Report Viewer's configuration to use the `puppet_detailed` HEC token, because detailed reports are pulled from Puppet and generated by the alert action in this application
- Update the advanced search macros to use the new values:
1. Open Advanced Search under the Settings -> Knowledge menu
2. Select `Search Macros`
3. Select `puppet_index` and change the definition to `index=puppet_data`, click save
4. Select `puppet_facts_index` and change the definition to `index=puppet_facts_data`, click save
5. Select `puppet_metrics_index` and change the definition to `index=puppet_metrics_data`, click save
6. Select `puppet_detailed_index` and change the definition to `index=puppet_detailed_data`, click save
- Reload the main view of the Puppet Report Viewer app, and you should see data, or perform the following search:
``` 
`puppet_all_index` sourcetype=puppet:*
```


More information
----------------

This addon will be updated frequently with more dashboards and views to data as feedback is gathered. Contact Puppet via the developer link and watch the [Puppet Community Office Hours calendar](https://puppet.com/community/office-hours) for future Splunk related events in our community [Slack](https://slack.puppet.com).
  