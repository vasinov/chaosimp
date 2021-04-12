import click

from cli_output import cli_success, automation_output
from clients.cloud_formation import CloudFormation
from name_constants import *
from imp_automation import ImpAutomation
from resource_names import cf_automation_name


@click.group()
@click.pass_context
def automations(ctx):
    pass


@automations.command()
@click.pass_context
def list(ctx):
    for automation in reversed(CloudFormation().list(TAG_VALUE_RESOURCE_TYPE_AUTOMATION)):
        automation_output(automation)


@automations.command()
@click.pass_context
@click.argument("name", type=click.STRING)
def get(ctx, name):
    automation_output(CloudFormation().get(cf_automation_name(name)))


@automations.command()
@click.pass_context
@click.option("--schedule", "-s", type=click.STRING, required=True)
@click.argument("name", type=click.STRING)
def create(ctx, schedule, name):
    cli_success("Creating new automation...")
    ImpAutomation(name, schedule).process(CloudFormation().create)


@automations.command()
@click.pass_context
@click.option("--schedule", "-s", type=click.STRING, required=True)
@click.argument("name", type=click.STRING)
def update(ctx, schedule, name):
    cli_success("Updating automation...")
    ImpAutomation(name, schedule).process(CloudFormation().update)


@automations.command()
@click.pass_context
@click.argument("name", type=click.STRING)
def delete(ctx, name):
    cli_success("Deleting automation...")
    CloudFormation().delete(cf_automation_name(name))