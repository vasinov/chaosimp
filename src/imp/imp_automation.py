from types import LambdaType

import yaml
from troposphere import Template
from cf_resource_builder import *
from cli_output import cli_error
from constants import *


class ImpAutomation:
    def __init__(self, name: str):
        self.name = name

    def process(self, processor: LambdaType):
        try:
            cf_template = Template("Imp automation.")

            return processor(cf_template_name(self.name), self.name, cf_template, TAG_VALUE_RESOURCE_TYPE_AUTOMATION)
        except yaml.YAMLError as e:
            cli_error(f'{type(e).__name__}: {e}')
