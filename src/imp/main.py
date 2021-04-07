import click
import os
from commands.config import config
from commands.templates import templates
from commands.experiments import experiments


@click.group()
@click.option(
    '--config', '-c',
    type=click.Path(),
    default='~/.imp',
)
@click.pass_context
def main(ctx, config):
    config_path = os.path.expanduser(config)
    ctx.obj = {

    }


if __name__ == "__main__":
    main.add_command(config)
    main.add_command(templates)
    main.add_command(experiments)
    main()
