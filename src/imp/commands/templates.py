import click
from clients.cloud_formation import *
from imp_template import ImpTemplate


@click.group()
@click.pass_context
def templates(ctx):
    pass


@templates.command()
@click.pass_context
@click.argument('name', type=click.STRING)
def get(ctx, name):
    click.echo(CloudFormation().get(ImpTemplate.template_name(name)))


@templates.command()
@click.pass_context
@click.option(
    '--path', '-p',
    type=click.Path(exists=True),
    required=True
)
@click.option(
    '--role-arn', '-r',
    type=click.STRING,
    required=True
)
@click.argument('name', type=click.STRING)
def create(ctx, path, role_arn, name):
    click.echo(ImpTemplate(path, name).process_template(role_arn, CloudFormation().create))


@templates.command()
@click.pass_context
@click.option(
    '--path', '-p',
    type=click.Path(exists=True),
    required=True
)
@click.option(
    '--role-arn', '-r',
    type=click.STRING,
    required=True
)
@click.argument('name', type=click.STRING)
def update(ctx, path, role_arn, name):
    click.echo(ImpTemplate(path, name).process_template(role_arn, CloudFormation().update))


@templates.command()
@click.pass_context
@click.argument('name', type=click.STRING)
def delete(ctx, name):
    click.echo(CloudFormation().delete(ImpTemplate.template_name(name)))
