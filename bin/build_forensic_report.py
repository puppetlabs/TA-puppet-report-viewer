
# encoding = utf-8
# Always put this line at the beginning of this file
import ta_puppet_report_forensics_declare

import os
import sys

from alert_actions_base import ModularAlertBase
import modalert_build_forensic_report_helper

class AlertActionWorkerbuild_forensic_report(ModularAlertBase):

    def __init__(self, ta_name, alert_name):
        super(AlertActionWorkerbuild_forensic_report, self).__init__(ta_name, alert_name)

    def validate_params(self):

        if not self.get_global_setting("puppet_enterprise_install"):
            self.log_error('puppet_enterprise_install is a mandatory setup parameter, but its value is None.')
            return False

        if not self.get_global_setting("auth_token"):
            self.log_error('auth_token is a mandatory setup parameter, but its value is None.')
            return False

        if not self.get_global_setting("splunk_server"):
            self.log_error('splunk_server is a mandatory setup parameter, but its value is None.')
            return False

        if not self.get_global_setting("hec_token"):
            self.log_error('hec_token is a mandatory setup parameter, but its value is None.')
            return False
        return True

    def process_event(self, *args, **kwargs):
        status = 0
        try:
            if not self.validate_params():
                return 3
            status = modalert_build_forensic_report_helper.process_event(self, *args, **kwargs)
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
    exitcode = AlertActionWorkerbuild_forensic_report("TA-puppet-report-forensics", "build_forensic_report").run(sys.argv)
    sys.exit(exitcode)
