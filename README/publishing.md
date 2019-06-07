Puppet Report Viewer Publishing Guide
==============

This documents how this plugin is published.

- Finalize testing
- Bundle this app up using the export options in the developing.md guide
- Import tar.gz into Splunk AddOn Builder for final validation preflight check
- Complete and fix validation steps if needed
- Make needed changes, tag build with final release number and publish a release in GitHub adding notes from releasenotes.md
- Rename file name to be .spl instead of .tar.gz
- Import .spl version to Splunk to verify that package installs properly
- Upload .spl to Splunkbase