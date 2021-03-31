import yaml
import re
from troposphere import Template

from lib.action_parsers.parser_factory import *
from lib.cf_template_builder import build_ssm_document
from lib.clients.cloud_formation import *


@click.group()
@click.pass_context
def templates(ctx):
    pass


@templates.command()
@click.pass_context
@click.option(
    '--path', '-p',
    type=click.Path(exists=True),
    required=True
)
@click.argument('name', type=click.STRING)
def create(ctx, path, name):
    __process_template(path, name, CloudFormation().create)


@templates.command()
@click.pass_context
@click.option(
    '--path', '-p',
    type=click.Path(exists=True),
    required=True
)
@click.argument('name', type=click.STRING)
def update(ctx, path, name):
    __process_template(path, name, CloudFormation().update)


@templates.command()
@click.pass_context
@click.argument('name', type=click.STRING)
def delete(ctx, name):
    CloudFormation().delete(__template_name(name))


def __process_template(path, name, processor):
    file_path = os.path.join(path, 'imp.yml')

    with open(click.format_filename(file_path), 'r') as stream:
        try:
            content = yaml.safe_load(stream)
            cf_template = Template()

            for action in content['actions']:
                action_parser = ParserFactory.to_action_parser(action)
                doc_name = re.sub(r'\W+', '', action["name"])

                cf_template.add_resource(
                    build_ssm_document(doc_name, action_parser.to_ssm_document(path))
                )

            processor(__template_name(name), cf_template)
        except yaml.YAMLError as e:
            click.secho(f'{type(e).__name__}: {e}', fg='red', err=True)


def __template_name(name):
    return f"imp-{name}"
