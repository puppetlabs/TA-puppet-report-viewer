Puppet Report Viewer Publishing Guide
==============

This documents how this plugin is published. This contains both steps for validating the app, uploading the app to Splunkbase, then tagging and releasing on the forge.

Build and validate:
An initial validation for building and sanity checks on the app.
- Create a clean installation of Splunk Enterprise
- Build and upload the TA-puppet-report-viewer from the master branch using this command:
  - 'COPYFILE_DISABLE=1 tar -C .. --exclude=".git" --exclude="local/" --exclude="metadata/local.meta" --exclude="tmpdir" -czvf tmpdir/TA-puppet-report-viewer.tar.gz TA-puppet-report-viewer`
- Rename file name to be .spl instead of .tar.gz (can be found inside the tmpdir/ dir)
- Download and install the app builder from Splunk - https://splunkbase.splunk.com/app/2962/ 
- Install the build '/tmpdir/TA-puppet-report-viewer.spl' on your Splunk installation using the 'manage app' section at the top left dropdown
- In the Splunk Add on Builder page choose the 'Other apps and add-ons', there you should see the Puppet Report Viewer you uploaded listed.
- Run the 'Validate & Package' option under the add-on. Choose the options that are in the bar by default. You may have to confirm your Splunk credentials before this will run.
- Hopefully with all being well the app should pass validation. If not work on the app until you are satisfied with the results from validation.

Upload the app to SplunkBase:
With the build you created and validated in the first section we will now aim to upload it to the SplunkBase.
- Navigate to the SplunkBase at https://splunkbase.splunk.com/apps/
- Navigate to 'My Account' - 'My Profile'
- Under your profile you should be able to see the Report Viewer. Click 'manage'. If the app isn't present contact one of the PIE team to get your Splunk user added as an Administrator of the app.
- Click 'New Release', upload the .spl file. This will validate the app before it uploads.
- You can set the visibility of the app in setup. If you want a straightforward release ensure you have set visible to true in the options on this page. Also ensure that you set the default to the new version if applicable.
- That should be you up and running live now you've uploded to splunkbase successfully!

The Modules Forge Release:
The last step we require is tagging the release in github.
- Do a release prep PR if required to update the CHANGELOG.
- Tag the build with the decided release number (according to semver) and push the tag up to git like the following example:
  - git tag -a (version) -m "(version)" <SHA> Example: git tag -a v2.2.0 -m "v2.2.0" 92488a003a6620555a499e15315c89849b0f150b
  - git push upstream --tags