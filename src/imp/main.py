import click
import os
from commands.templates import templates


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
    main.add_command(templates)
    main()
