## Developing addon builders

In order to load this module properly into the Splunk Add-On builder for development, the following needs to happen:

- Checkout the branch you want to work on
- tar.gz the directory
- Go to the splunk addon builder
- Delete a previous version of the add-on if it exists
- Import this version

```
$ git checkout -b 'my working branch'
$ COPYFILE_DISABLE=1 tar -C .. --exclude=".git" --exclude="local/" --exclude="metadata/local.meta" --exclude="tmpdir" -czvf tmpdir/TA-puppet-report-viewer.tar.gz TA-puppet-report-viewer
```

To add your finished work back to the repo:
- Export the build from the Splunk Add-On tool
- Move the downloaded tar.gz to tmpdir
- Expand the export the export in tmpdir
- sync the local repo with the tmpdir contents
- proceed with git commits as needed, etc

```
$ cd tmpdir
$ tar xzvf TA-puppet-report-viewer_2_0_1_export.tgz
$ cd ..
$ rsync -vr tmpdir/TA-puppet-report-viewer_2_0_1_export/* ./
```
