from types import LambdaType

import yaml
from troposphere import Template

from resource_builders.cf_automation_resources import build_assume_role, build_lambda_function, build_rule, \
    build_lambda_permission
from cli_output import cli_error
from name_constants import *
from resource_names import cf_automation_name


class ImpAutomation:
    def __init__(self, name: str, schedule: str):
        self.name = name
        self.schedule = schedule

    def process(self, processor: LambdaType):
        try:
            cf_template = Template("Imp automation.")

            cf_template.add_resource(build_assume_role(self.name))
            cf_template.add_resource(build_lambda_function(self.name))
            cf_template.add_resource(build_rule(self.name, self.schedule))
            cf_template.add_resource(build_lambda_permission(self.name))

            return processor(
                cf_automation_name(self.name), self.name, cf_template, TAG_VALUE_RESOURCE_TYPE_AUTOMATION, True
            )
        except yaml.YAMLError as e:
            cli_error(f'{type(e).__name__}: {e}')
