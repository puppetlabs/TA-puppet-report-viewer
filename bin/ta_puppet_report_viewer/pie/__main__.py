# encoding = utf-8

import json
import sys

if __name__ == "__main__":
  args = json.load(sys.stdin)
  
  token = genauthtoken(args['username'], args['password'], args['label'], args['rbacurl'])
  print(token)
  
  job = reqtask(args['node'], args['task'], args['parameters'], token, args['environment'], args['orchurl'])
  print(job['name'])
  
  result = getjobresult(job['name'], token, args['orchurl'])

  print(result)

  deploy = reqdeploy(args['node'], True, token, args['environment'], args['orchurl'])

  print(deploy['name'])

  puppetreport = getjobresult(deploy['name'], token, args['orchurl'])

  print(puppetreport)

  for item in puppetreport['items']:
    uuid = item['transaction_uuid']
    print(uuid)
    report = getpuppetreport(uuid, args['pdburl'], token)
    print(report)
