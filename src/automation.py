from types import LambdaType
from troposphere import Template
from src.cf_resource_builders.automation import *
from src.cli_output import cli_error
from src.name_constants import *
from src.resource_names import cf_automation_name


class Automation:
    def __init__(self, name: str, schedule: str, template_name: str, image: str):
        self.name = name
        self.schedule = schedule
        self.template_name = template_name
        self.image = image

    def process(self, processor: LambdaType):
        try:
            cf_template = Template("Imp automation.")

            cf_template.add_resource(build_assume_role(self.name))
            cf_template.add_resource(build_lambda_function(self.name, self.image))
            cf_template.add_resource(build_rule(self.name, self.schedule, self.template_name))
            cf_template.add_resource(build_lambda_permission(self.name))

            return processor(
                cf_automation_name(self.name), self.name, cf_template, TAG_VALUE_RESOURCE_TYPE_AUTOMATION, True
            )
        except Exception as e:
            cli_error(f'{type(e).__name__}: {e}')
