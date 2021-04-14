import click
from src.cli_output import experiment_output, cli_success
from src.clients.fis import *


@click.group()
@click.pass_context
def experiments(ctx):
    pass


@experiments.command()
@click.pass_context
@click.argument("template_name", type=click.STRING, required=False)
def list(ctx, template_name):
    for experiment in reversed(Fis().list(template_name)):
        experiment_output(experiment)


@experiments.command()
@click.pass_context
@click.argument("id", type=click.STRING)
def get_by_id(ctx, id):
    experiment_output(Fis().get_by_id(id))


@experiments.command()
@click.pass_context
@click.argument("name", type=click.STRING)
def get(ctx, name):
    experiment_output(Fis().get_latest_by_name(name))


@experiments.command()
@click.pass_context
@click.option("--template", "-t", type=click.STRING, required=True)
@click.argument("name", type=click.STRING)
def start(ctx, template, name):
    experiment_output(Fis().start(template, name))


@experiments.command()
@click.pass_context
@click.argument("id", type=click.STRING)
def stop(ctx, id):
    cli_success("Stopping experiment...")
    Fis().stop(id)
