Release Notes
==============

1.5.1:
New Features:
- Full dashboard updates
- Support for Facts sourcetype (puppet:facts), and dashboards to use it
- Introduces "Report Builder" page to help a user build reports and then craft custom search from the iterface to use for alerts or their own uses
- Introduces Advanced Search macros to allow for customized indexs without requiring to modify the app. See Advanced Configuration section of the readme
- Add's sourcetypes of puppet:action, puppet:metrics, for future use
- Example Alert added, the search to generate a detailed report for any summary report that isn't "unchanged" has been added to the app, but set as disabled

Fixes:
- Duplicate item entry fixed, sourcetype's are now configured to extract KV from json only once
- [Updated documentation](https://github.com/puppetlabs/ta-puppet-report-viewer)

