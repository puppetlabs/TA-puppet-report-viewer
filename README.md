# Puppet Report Viewer

##### Table of Contents

1. [Description](#description)
2. [Configuration](#configuration)
3. [Advanced Configuration](#advanced-configuration)
4. [Troubleshooting and Verification](#troubleshooting-and-verification)

## Description

This Splunk app provides views into the status of Puppet installations that are configured to send reports and metrics with the [`splunk_hec`](https://forge.puppet.com/puppetlabs/splunk_hec) and [`puppet_metrics_collector`](https://forge.puppet.com/puppetlabs/puppet_metrics_collector) Puppet modules.

## Configuration

Once the application has been installed follow the steps below to configure the [Puppet Report Viewer](https://splunkbase.splunk.com/app/4413/):

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

  ![hec_token](https://raw.githubusercontent.com/puppetlabs/puppetlabs-splunk_hec/main/docs/images/hec_token.png)

After configuring both `splunk_hec` and the `puppet_metrics_collector` the Overview tab will start showing data from Puppet reports, while the Metrics tab will start displaying graphs related to a number of useful Puppet metrics.

![Reports Overview](https://raw.githubusercontent.com/puppetlabs/TA-puppet-report-viewer/main/TA-puppet-report-viewer/README/img/overview.png)

![Metrics](https://raw.githubusercontent.com/puppetlabs/TA-puppet-report-viewer/main/TA-puppet-report-viewer/README/img/metrics.png)

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

## Troubleshooting and Verification

If the Puppet Report Viewer does not appear to show any data after you have followed the configuration steps for both this app and the [splunk_hec](https://github.com/puppetlabs/puppetlabs-splunk_hec) module; first check that data is being successfully sent to the Splunk server by following the [troubleshooting and verification](https://github.com/puppetlabs/puppetlabs-splunk_hec/blob/main/docs/troubleshooting_and_verification.md) steps in the `splunk_hec` documentation.

If events in the `puppet:detailed` source type are not showing up in search, it means that the "Generate a Detailed Report" Alert is not configured properly with the [Puppet Alert Actions](https://splunkbase.splunk.com/app/4928/) add-on. If this Alert is enabled, and the aforementioned add-on is configured, you can view the logs with the following Splunk search:

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
