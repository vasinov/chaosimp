from cli_output import template_output, cli_success
from clients.cloud_formation import *
from imp_template import *


@click.group()
@click.pass_context
def templates(ctx):
    pass


@templates.command()
@click.pass_context
def list(ctx):
    for template in reversed(CloudFormation().list()):
        template_output(template)

@templates.command()
@click.pass_context
@click.argument("name", type=click.STRING)
def get(ctx, name):
    template_output(CloudFormation().get(cf_template_name(name)))


@templates.command()
@click.pass_context
@click.option("--path", "-p", type=click.Path(exists=True), required=True)
@click.option("--role-arn", "-r", type=click.STRING, required=True)
@click.argument("name", type=click.STRING)
def create(ctx, path, role_arn, name):
    ImpTemplate(path, name).process(role_arn, CloudFormation().create)
    cli_success("Creating new template...")


@templates.command()
@click.pass_context
@click.option("--path", "-p", type=click.Path(exists=True), required=True)
@click.option("--role-arn", "-r", type=click.STRING,  required=True)
@click.argument("name", type=click.STRING)
def update(ctx, path, role_arn, name):
    ImpTemplate(path, name).process(role_arn, CloudFormation().update)
    cli_success("Updating template...")


@templates.command()
@click.pass_context
@click.argument("name", type=click.STRING)
def delete(ctx, name):
    click.echo(CloudFormation().delete(cf_template_name(name)))
    cli_success("Deleting template...")
