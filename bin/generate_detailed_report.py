
# encoding = utf-8
# Always put this line at the beginning of this file
import ta_puppet_report_viewer_declare

import os
import sys

from alert_actions_base import ModularAlertBase
import modalert_generate_detailed_report_helper

class AlertActionWorkergenerate_detailed_report(ModularAlertBase):
    def __init__(self, ta_name, alert_name):
        super(AlertActionWorkergenerate_detailed_report, self).__init__(ta_name, alert_name)

    def verify_global_setting(setting_name):
        if not self.get_global_setting(setting_name):
            self.log_error('{0} is a mandatory setup parameter, but its value is None.'.format(setting_name))
            return False
        return True

    def validate_params(self):
        global_settings = ['puppet_enterprise_console', 'puppet_read_user', 'puppet_read_user_pass', 'splunk_hec_url', 'splunk_hec_token']

        for setting_name in global_settings:
            if not verify_global_setting(setting_name):
                return False

        return True

    def process_event(self, *args, **kwargs):
        status = 0
        try:
            if not self.validate_params():
                return 3
            status = modalert_generate_detailed_report_helper.process_event(self, *args, **kwargs)
        except (AttributeError, TypeError) as ae:
            self.log_error("Error: {}. Please double check spelling and also verify that a compatible version of Splunk_SA_CIM is installed.".format(ae.message))
            return 4
        except Exception as e:
            msg = "Unexpected error: {}."
            if e.message:
                self.log_error(msg.format(e.message))
            else:
                import traceback
                self.log_error(msg.format(traceback.format_exc()))
            return 5
        return status

if __name__ == "__main__":
    exitcode = AlertActionWorkergenerate_detailed_report("TA-puppet-report-viewer", "generate_detailed_report").run(sys.argv)
    sys.exit(exitcode)
