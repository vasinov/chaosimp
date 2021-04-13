import os
from types import LambdaType
from troposphere import Template
from cf_resource_builders.automation import *
from cli_output import cli_error
from name_constants import *
from resource_names import cf_automation_name


class ImpAutomation:
    def __init__(self, name: str, schedule: str, template_name: str):
        self.name = name
        self.schedule = schedule
        self.template_name = template_name

        with open(os.path.join("src/imp/cf_resource_builders/data/aws_lambda_fis_experiment.py"), 'r') as stream:
            self.function_content = stream.read()

    def process(self, processor: LambdaType):
        try:
            cf_template = Template("Imp automation.")

            cf_template.add_resource(build_assume_role(self.name))
            cf_template.add_resource(build_lambda_function(self.name, self.function_content))
            cf_template.add_resource(build_rule(self.name, self.schedule, self.template_name))
            cf_template.add_resource(build_lambda_permission(self.name))

            return processor(
                cf_automation_name(self.name), self.name, cf_template, TAG_VALUE_RESOURCE_TYPE_AUTOMATION, True
            )
        except Exception as e:
            cli_error(f'{type(e).__name__}: {e}')
