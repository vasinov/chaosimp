import click
from cli_output import template_output, cli_success
from clients.cloud_formation import *
from config_manager import ConfigManager, TEMPLATE_ROLE_ARN_KEY
from imp_template import *


@click.group()
@click.pass_context
def templates(ctx):
    pass


@templates.command()
@click.pass_context
def list(ctx):
    for template in reversed(CloudFormation().list(TAG_VALUE_RESOURCE_TYPE_TEMPLATE)):
        template_output(template)


@templates.command()
@click.pass_context
@click.argument("name", type=click.STRING)
def get(ctx, name):
    template_output(CloudFormation().get(cf_template_name(name)))


@templates.command()
@click.pass_context
@click.option("--path", "-p", type=click.Path(exists=True), required=True)
@click.option("--role-arn", "-r", type=click.STRING, required=not ConfigManager().get(TEMPLATE_ROLE_ARN_KEY))
@click.argument("name", type=click.STRING)
def create(ctx, path, role_arn, name):
    role_arn = role_arn or ConfigManager().get(TEMPLATE_ROLE_ARN_KEY)

    cli_success("Creating new template...")
    ImpTemplate(path, name).process(role_arn, CloudFormation().create)


@templates.command()
@click.pass_context
@click.option("--path", "-p", type=click.Path(exists=True), required=True)
@click.option("--role-arn", "-r", type=click.STRING,  required=False)
@click.argument("name", type=click.STRING)
def update(ctx, path, role_arn, name):
    role_arn = role_arn or ConfigManager().get(TEMPLATE_ROLE_ARN_KEY)

    cli_success("Updating template...")
    ImpTemplate(path, name).process(role_arn, CloudFormation().update)


@templates.command()
@click.pass_context
@click.argument("name", type=click.STRING)
def delete(ctx, name):
    cli_success("Deleting template...")
    CloudFormation().delete(cf_template_name(name))
