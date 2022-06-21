# Puppet Report Viewer Publishing Guide

This document contains steps to publish the Puppet Report Viewer app for Splunk to Splunkbase.

## Build app package

First open a release prep PR to update the following files:

  * `app.manifest`
  * `default/app.conf`
  * `README.md`
  * `readme/CHANGELOG.md`

Tagging the release in GitHub will trigger the [release workflow](https://github.com/puppetlabs/TA-puppet-report-viewer/actions/workflows/release.yml) to build the app package.

Tag the release with the appropriate version ID and push the tag upstream:

  * `git tag <VERSION> <SHA>` (**e.g.** `git tag v4.0.0 92488a003a6620555a499e15315c89849b0f150b`)
  * `git push upstream --tags`

**Note**: The package is uploaded to GitHub as a `.zip` file. As such, you will first need to run the `unzip` command to expose the `.tar.gz` file.

## Manually upload the app to Splunkbase

After unzipping the file to a `.tar.gz` perform the following steps:

  * Navigate to [Splunkbase](https://splunkbase.splunk.com) and log in.
  * Navigate to **My Account** -> **My Profile**.
    * Under your profile you will see our Splunk applications.
    * Select **manage** next to the application name.
    * On the right, select **New Version**.
    * Upload the `.tar.gz` file.

The new release should appear in the list of available versions. Select the release to finalize the upload:

  * Copy the latest release notes from the `CHANGELOG`.
  * If needed, modify the **Splunk Version Compatibility** matrix.
  * Select **Make my release visible** and click **save**.
  * Next to the version number, select **DEFAULT** to ensure the latest version is being served.

Lastly, if there were any changes to the `README` you will want to add those to the application **Details** in the left navigation pane.
