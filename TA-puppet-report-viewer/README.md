# Puppet Report Viewer

##### Table of Contents

1. [Description](#description)
2. [Configuration](#configuration)
3. [Advanced Configuration](#advanced-configuration)
4. [Example Searches](#example-log-searches)
5. [Troubleshooting and Verification](#troubleshooting-and-verification)

## Description

This Splunk app provides custom source types and views into the status of Puppet installations that are configured to send reports, facts and metrics with the [`splunk_hec`](https://forge.puppet.com/puppetlabs/splunk_hec), [`puppet_metrics_collector`](https://forge.puppet.com/puppetlabs/puppet_metrics_collector) and [`pe_status_check`](https://forge.puppet.com/puppetlabs/pe_status_check) Puppet modules.

You can take action on this data by connecting a Splunk installation to the PE Orchestration service via the [Puppet Alert Orchestrator add-on for Splunk](https://splunkbase.splunk.com/app/7318/).

## Configuration

Once the application has been installed follow the steps below to configure the [Puppet Report Viewer app for Splunk](https://github.com/puppetlabs/TA-puppet-report-viewer):

Create an Splunk HEC token for the app:

  * Select Puppet Report Viewer from the App dropdown in the Splunk console.
  * Navigate to `Settings` > `Data Input`.
  * Add a new `HTTP Event Collector` token with a name of your choice.
  * Ensure `indexer acknowledgement` is **not** enabled.
  * Click Next and set the source type to **Automatic**.
  * Add the `main` index
  * Set the **Default Index** to `main`.
  * Click **Review** and then **Submit**.
  * When complete the HEC token should look something like this:

  ![hec_token](297570e2-f1b0-11ec-ada5-56570d6f424e.png)

After configuring `splunk_hec`, `puppet_metrics_collector`, and `pe_status_check` the Overview tab will start showing data from Puppet reports, while the PE Metrics tab will start displaying graphs related to a number of useful Puppet metrics and results of status checks.

![Reports Overview](1304dd3e-f1b0-11ec-bf36-3691ecc87010.png)

![Metrics](183aad88-f1b0-11ec-9fc7-a60803d6ab2e.png)

### Custom Source Types

This app includes the following custom source types:

  * Data from **puppetlabs-splunk_hec** module:
    * `puppet:facts`
    * `puppet:summary`
  
  * Data from **puppetlabs-puppet\_metrics\_collector** module:
    * `puppet:metrics`
 
  * Data from **puppetlabs-pe\_event\_forwarding** module:
    * `puppet:activities_classifier`
    * `puppet:activities_code_manager`
    * `puppet:activities_console`
    * `puppet:activities_rbac`
    * `puppet:activity`
    * `puppet:events_summary`
    * `puppet:jobs`

  * Data from **Puppet Alert Orchestrator add-on for Splunk**:
    * `puppet:action`
    * `puppet:bolt`
    * `puppet:detailed`
 
  * Data from Puppet infrastructure nodes via Splunk Forwarder:
    * `puppet:service_logs`
    * `puppet:access_logs`


**Note**: Access and Service logs for the following Puppet services are currently supported.

  * PE Console
  * PE Orchestrator
  * PuppetDB
  * Puppet Server

## Advanced Configuration

All dashboard views support using custom indexes for storing event data. The searches assume each sourcetype can be stored in it's own index. There is one top level macro (`puppet_index`) which defaults to `""`.

As such, you can specify different HEC tokens for Summary Reports, Facts, and Metrics in `splunk_hec`. If you configure multiple HEC tokens to utilize different indexes, change the `index` value in the dashboards to reflect this.

##### Example Configuration: 

Create five indexes named `puppet_data`, `puppet_summary_data`, `puppet_facts_data`, `puppet_metrics_data`, and `puppet_detailed_data`.

Create five HEC tokens:

  * `puppet_data` with sourcetype of `automatic` and the index `puppet_data`.
  * `puppet_summary` with sourcetype of `puppet:summary` and the index `puppet_summary_data`.
  * `puppet_facts` with sourcetype of `puppet:facts` and the index of `puppet_facts_data`.
  * `puppet_metrics` with sourcetype of `puppet:metrics` and the index of `puppet_metrics_data`.
  * `puppet_detailed` with sourcetype of `puppet:detailed` and the index of `puppet_detailed_data`.

Configure the `splunk_hec` module with the following token parameters:

  * `splunk_hec::token` with the `puppet_data` token value.
  * `splunk_hec::token_summary` with the `puppet_summary` token value.
  * `splunk_hec::token_facts` with the `puppet_facts` token value.
  * `splunk_hec::token_metrics` with the `puppet_metrics` token value.

Update the search macros to use the new values:

* Open **Advanced Search** under `Settings` > `Knowledge`.
* Select `Search Macros`.
* Select `puppet_index` and change the definition to `index=puppet_data`, click save.
* Select `puppet_summary_index` and change the definition to `index=puppet_summary_data`, click save.
* Select `puppet_facts_index` and change the definition to `index=puppet_facts_data`, click save.
* Select `puppet_metrics_index` and change the definition to `index=puppet_metrics_data`, click save.
* Select `puppet_detailed_index` and change the definition to `index=puppet_detailed_data`, click save.

Upon reloading the **Overview** tab in the Puppet Report Viewer app, and you should begin seeing data. Alternatively, perform the following search:

``` 
`puppet_all_index` sourcetype=puppet:*
```

## Example Log Searches

### Puppet Server

**Top API Calls**

```
`puppet_logs_index` sourcetype=puppet:access_logs source=*puppetserver-access.log
| rename request as Endpoint
| chart avg(elapsed_time) as "Time (ms)" by Endpoint
| sort - "Time (ms)"
```

**Longest Compile Time**

```
`puppet_logs_index` sourcetype=puppet:access_logs source=*puppetserver-access.log method=POST request=/puppet/v3/catalog*
| chart max(elapsed_time) as "Time (ms)" by client
| sort - "Time (ms)"
```

### PuppetDB

**Longest Query Time**

```
`puppet_logs_index` sourcetype=puppet:access_logs source=*puppetdb-access.log request=/pdb/query/*
| chart max(elapsed_time) as "Time (ms)" by client
| sort - "Time (ms)"
```

**Sync Issues**

```
`puppet_logs_index` sourcetype=puppet:service_logs service=sync log_level=WARN OR ERROR
| chart values(message) as Message by log_level
```

## Troubleshooting and Verification

If the Puppet Report Viewer does not appear to show any data after you have followed the configuration steps for both this app and the [splunk_hec](https://github.com/puppetlabs/puppetlabs-splunk_hec) module; first check that data is being successfully sent to the Splunk server by following the [troubleshooting and verification](https://github.com/puppetlabs/puppetlabs-splunk_hec/blob/main/docs/troubleshooting_and_verification.md) steps in the `splunk_hec` documentation.

If events in the `puppet:detailed` source type is not showing up in search, it means that the "Generate a Detailed Report" Alert is not configured properly with the [Puppet Alert Orchestrator](https://splunkbase.splunk.com/app/7318/) add-on. If this Alert is enabled, and the aforementioned add-on is configured, you can view the logs with the following Splunk search:

```
index=_internal sourcetype=splunkd component=sendmodalert (action="puppet_run_task_investigate" OR action="puppet_run_task" OR action="puppet_run_task_act" OR action="puppet_generate_detailed_report")
```

There is also a view into the Alert Actions logs under the Actions tab which will show these searches as well.

If there are no error messages, verify that the configured HEC works can be used to submit a report manually:

```
$ curl -k -H "Authorization: Splunk <yourHECtoken>" https://localhost:8088/services/collector/event -d '{"sourcetype": "puppet:detailed", "event": "exampletest"}'
```
The endpoint will respond with either a success or an error message. Follow steps in the [HTTP Event Collector](https://docs.splunk.com/Documentation/Splunk/latest/Data/UsetheHTTPEventCollector) documentation to resolve issues with the HEC endpoint.

If there are other error messages in the logs related to PE RBAC tokens from the Puppet side, run the following command to query the PuppetDB API:

```
curl -k 'https://<your.puppetdb.server>:8081/pdb/query/v4/nodes' -H "X-Authentication: <token contents>"
```
