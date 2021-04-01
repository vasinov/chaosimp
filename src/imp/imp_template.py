import humps
import yaml
from troposphere import Template

from action_parsers.parser_factory import *
from cf_resource_builder import *


class ImpTemplate:
    def __init__(self, path, name):
        self.path = path
        self.name = name

        file_path = os.path.join(path, 'imp.yml')

        with open(click.format_filename(file_path), 'r') as stream:
            self.content = yaml.safe_load(stream)

    @staticmethod
    def template_name(name):
        return f"imp-{name}"

    def process_template(self, role_arn, processor):
        try:
            cf_template = Template()

            for action in self.content['actions']:
                action_parser = to_action_parser(action)

                cf_template.add_resource(
                    build_ssm_document(
                        humps.pascalize(f"ssm-doc-{action['name']}"), action_parser.to_ssm_document(self.path)
                    )
                )

                cf_template.add_resource(
                    build_fis_template(
                        humps.pascalize(f"fis-template-{action['name']}"),
                        role_arn,
                        self.get_targets(self.content["targets"], action["targets"])
                    )
                )

            processor(self.template_name(self.name), cf_template)
        except yaml.YAMLError as e:
            click.secho(f'{type(e).__name__}: {e}', fg='red', err=True)

    def get_targets(self, targets, target_names):
        return list(filter(lambda t: (t["name"] in target_names), targets))
