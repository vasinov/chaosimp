from types import LambdaType

import yaml
from troposphere import Template
from action_parsers.imp_run_script_parser import *
from cf_resource_builder import *
from cli_output import cli_error
from constants import *


class ImpTemplate:
    def __init__(self, path: str, name: str):
        self.path = path
        self.name = name

        file_path = os.path.join(path, 'imp.yml')

        with open(file_path, 'r') as stream:
            self.data = yaml.safe_load(stream)

    def process(self, role_arn: str, processor: LambdaType):
        try:
            ssm_docs = []
            cf_template = Template(self.data["Description"])

            # First, add SSM documents

            for action in self.data['Actions']:
                if action['Type'] == ACTION_TYPE_IMP_RUN_SCRIPT:
                    parser = ImpRunScriptParser(action.get("Name"), action.get("Document", {}).get("Path"))
                    ssm_document = build_ssm_document(
                        self.name,
                        action.get("Name"),
                        parser.to_ssm_document(self.path, action.get("Document", {}).get("Parameters", []))
                    )

                    cf_template.add_resource(ssm_document)

                    ssm_docs.append(action.get("Name"))

            # Now, create FIS templates

            cf_template.add_resource(
                build_fis_template(
                    self.name,
                    role_arn,
                    self.data,
                    ssm_docs
                )
            )

            return processor(cf_template_name(self.name), self.name, cf_template, TAG_VALUE_RESOURCE_TYPE_TEMPLATE)
        except yaml.YAMLError as e:
            cli_error(f'{type(e).__name__}: {e}')
