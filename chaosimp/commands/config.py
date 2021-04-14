import click

from chaosimp.cli_output import cli_info, cli_warn, cli_success
from chaosimp.config_manager import ConfigManager


@click.group()
@click.pass_context
def config(ctx):
    pass


@config.command()
@click.pass_context
def list(ctx):
    loaded_config = ConfigManager().list()

    if loaded_config:
        for key, value in loaded_config.items():
            cli_info(f"{key}: {value}")
    else:
        cli_warn("Config file not found.")


@config.command()
@click.pass_context
@click.argument("key", type=click.STRING)
def get(ctx, key):
    cli_info(ConfigManager().get(key))


@config.command()
@click.pass_context
@click.argument("key", type=click.STRING)
@click.argument("value", type=click.STRING)
def set(ctx, key, value):
    if ConfigManager().set(key, value):
        cli_success(f"'{key}' was set to '{value}'")
