import click
from chaosimp.commands.automations import automations
from chaosimp.commands.config import config
from chaosimp.commands.experiments import experiments
from chaosimp.commands.templates import templates


@click.group()
@click.option(
    '--config', '-c',
    type=click.Path(),
    default='~/.imp',
)
@click.pass_context
def main(ctx, config):
    ctx.obj = {}


main.add_command(config)
main.add_command(automations)
main.add_command(templates)
main.add_command(experiments)

if __name__ == "__main__":
    main()
