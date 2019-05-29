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

More information
----------------

More information
----------------

This addon will be updated frequently with more dashboards and views to data as feedback is gathered. Contact Puppet via the developer link and watch the [Puppet Community Office Hours calendar](https://puppet.com/community/office-hours) for future Splunk related events in our community [Slack](https://slack.puppet.com).
  