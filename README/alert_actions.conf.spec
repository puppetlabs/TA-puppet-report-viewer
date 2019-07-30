
[generate_detailed_report]
param.transaction_uuid = <string> Transaction UUID.

[puppet_run_task_investigate]
param.bolt_investigate_name = <list> Investigate. It's a required parameter. It's default value is lastlogin.
param.bolt_investigate_target = <string> Host. It's a required parameter. It's default value is $result.host$.

[puppet_run_task]
param.task_name = <string> Task. It's a required parameter.
param.puppet_environment = <string> Puppet Environment.  It's default value is production.
param.bolt_target = <string> Host. It's a required parameter. It's default value is $result.host$.
param.task_parameters = <string> Task Parameters.

[puppet_run_task_act]
param.bolt_act_name = <list> Perform Action. It's a required parameter. It's default value is service.
param.bolt_act_target = <string> Host. It's a required parameter. It's default value is $result.host$.

