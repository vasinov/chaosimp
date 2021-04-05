import yaml
from troposphere import Template
from action_parsers.imp_run_script_parser import *
from cf_resource_builder import *
from constants import *


class ImpTemplate:
    def __init__(self, path, name):
        self.path = path
        self.name = name

        file_path = os.path.join(path, 'imp.yml')

        with open(click.format_filename(file_path), 'r') as stream:
            self.content = yaml.safe_load(stream)

    def process(self, role_arn, processor):
        try:
            ssm_docs = []
            cf_template = Template()

            for action in self.content['actions']:
                if action['type'] == ACTION_TYPE_IMP_RUN_SCRIPT:
                    parser = ImpRunScriptParser(action["name"], action["path"])
                    ssm_document = build_ssm_document(
                        self.name,
                        action['name'], parser.to_ssm_document(self.path)
                    )

                    cf_template.add_resource(ssm_document)

                    ssm_docs.append(action["name"])

            cf_template.add_resource(
                build_fis_template(
                    self.name,
                    role_arn,
                    self.content["targets"],
                    self.content["actions"],
                    ssm_docs
                )
            )

            processor(cf_template_name(self.name), cf_template)
        except yaml.YAMLError as e:
            click.secho(f'{type(e).__name__}: {e}', fg='red', err=True)
