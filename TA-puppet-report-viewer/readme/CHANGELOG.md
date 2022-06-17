# Release Notes

## Version 4.0.0

**Breaking Changes**:

  * This release adds new dashboards that depend on the [status indicator visualization](https://splunkbase.splunk.com/app/3119/).

**New Features**:

  * Changes to Metrics dropdowns for better filtering.
  * Changes to Metrics view to chart a number of metrics `by host` for comparison view.
  * New **PE Metrics** tab contains Metrics and Status Checks.
    * Adds PE Status Check Dashboards
      * **Note**: Requires the [`puppetlabs-pe_status_check`](https://forge.puppet.com/modules/puppetlabs/pe_status_check) module.

**Fixes**:

  * Removes conditional filtering for PostgreSQL metric dashboards preventing them from properly loading.

## Version 3.1.2

**New Features**:

  * New dashboard panels added to the metrics tab which track a number of useful metrics for PostgreSQL.
Fixes:

  * Reorganized the order of the navigation tabs in the app.

## Version 3.1.1

**New Features**:

  * `puppet:activities_console`, and `puppet:activities_code_manager` source types added.

**Fixes**:

  * In a distributed Splunk installation, it was previously required to have this application installed on both the Search Heads and the Indexers to ensure that the source types were available across the installation. Removing the `AUTO_KV_JSON` setting to allow for the default value (true); JSON parsing now occurs at search-time.

## Version 3.1.0

**New Features**:

  * This version replaces the default dashboards available in the Metrics tab with all new dashboards; measuring a number of useful metrics for Puppet Server, PuppetDB and Orchestrator.

## Version 3.0.3

**New Features**:

  * `puppet:jobs`, `puppet:activities_rbac`, and `puppet:activities_classifier` source types added.

**Fixes**:

  * Some of the panels in the Overview dashboard still contain the "X" button in the upper right to close the pop-up panel when you click on the primary panel. Some of the other panels lost the X.

  * Changed the drilldown to set/unset the token that shows the drilldown panel on click. Effect of the change is that clicking on the panel with the drilldown hidden shows the drilldown. Clicking on the panel with the drilldown showing hides the drilldown.

  * Also removed the remaining "X" buttons.

  * Standardize some visual formatting - moved "units" to "captions" on the images to "hosts, seconds, etc" shows up underneath the reported numbers, rather than next to them, removed odd height settings.

## Version 3.0.2

**New Features**:

  * `puppet:events_summary` and `puppet:activity` source types added.

**Fixes**:

  * The searches that are used in the Overview tab to display resources under the "# of Resources" element and associated table used to display the number of reports. They have been corrected to display the number of resources.

  * Development workflow updated.

## Version 3.0.1

**Breaking Changes**:

  * Alert Actions are now moved to https://github.com/puppetlabs/TA-puppet-alert-actions for better compatibility of this App for users who don't use or need the add-on.

## Version 2.0.0

**Breaking Changes**:

  * The alert action named `Generate detailed report` has been renamed `Generate a detailed Puppet report` to make it more specific. The internal name of the action has been renamed to `puppet_generate_detailed_report` from `generate_detailed_report` to prevent confusion with out alert actions and to ensure consistency with other. You will need to update existing searches using this action to use the new name, but no other changes to the searches is required.

  * Alert Actions will fail until Puppet Username is provided instead of PE auth token.

  * Full URIs are now required instead of just hostnames to add more flexibility. The authorization methods (http support and custom ports) but you will need to redo your app configuration before alert actions resume functioning.

  * Searches defaulting to main and not using the index macros will stop updating if you move the corressponding puppet data to an index but don't change the search

**New Features**:

  * Built in support for running Bolt Tasks in Puppet Enterprise from Splunk.

  * Metrics tab to show PE metric data if metrics are configured.

  * Actions Tab in dashboard added to show logs and status of any of this applications alert actions for debugging or auditing.

  * Support for Puppet Username/Password instead of auth token.

  * All searches support per source type indexes.

**Fixes**:

  * Alert actions work with custom parameters.

  * Before there was no way to see if your alerts were working easily, now they publish information to the `puppet:action` source type.

## Version 1.5.1

**New Features**:

  * Full dashboard updates.

  * Support for Facts source type (`puppet:facts`), and dashboards to use it.

  * Introduces "Report Builder" page to help a user build reports and then craft custom search from the interface to use for alerts or their own uses.

  * Introduces Advanced Search macros to allow for customized indexes without requiring to modify the app. See Advanced Configuration section of the readme.

  * Add's source types of `puppet:action`, `puppet:metrics`, for future use.

  * Example Alert added, the search to generate a detailed report for any summary report that isn't "unchanged" has been added to the app, but set as disabled.

**Fixes**:

  * Duplicate item entry fixed, source type's are now configured to extract KV from JSON only once.

  * [Updated Documentation](https://github.com/puppetlabs/ta-puppet-report-viewer)

