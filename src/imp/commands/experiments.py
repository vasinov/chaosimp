from clients.fis import *
from imp_template import *


@click.group()
@click.pass_context
def experiments(ctx):
    pass


@experiments.command()
@click.pass_context
@click.argument('name', type=click.STRING)
def list(ctx, name):
    click.echo(Fis().list(name))


@experiments.command()
@click.pass_context
@click.option(
    '--template', '-t',
    type=click.STRING,
    required=True
)
@click.argument('name', type=click.STRING)
def start(ctx, template, name):
    click.echo(Fis().start(template, name))
