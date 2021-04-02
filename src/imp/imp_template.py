import yaml
from troposphere import Template

from action_parsers.imp_run_script_parser import *
from cf_resource_builder import *


def template_name(name):
    return f"imp-{name}"


class ImpTemplate:
    def __init__(self, path, name):
        self.path = path
        self.name = name

        file_path = os.path.join(path, 'imp.yml')

        with open(click.format_filename(file_path), 'r') as stream:
            self.content = yaml.safe_load(stream)

    def process(self, role_arn, processor):
        try:
            cf_template = Template()

            for action in self.content['actions']:
                if action['type'] == "imp:run-script":
                    parser = ImpRunScriptParser(action["name"], action["path"])

                    cf_template.add_resource(
                        build_ssm_document(
                            humps.pascalize(f"ssm-doc-{action['name']}"), parser.to_ssm_document(self.path)
                        )
                    )

            cf_template.add_resource(
                build_fis_template(
                    humps.pascalize(f"fis-template-{self.name}"),
                    role_arn,
                    self.content["targets"]
                )
            )

            processor(template_name(self.name), cf_template)
        except yaml.YAMLError as e:
            click.secho(f'{type(e).__name__}: {e}', fg='red', err=True)
