import click
import os

from commands.targets import targets

@click.group()
@click.option(
    '--config', '-c',
    type = click.Path(),
    default = '~/.imp',
)
@click.option(
    '--s3-bucket',
    required = True
)
@click.pass_context
def main(ctx, config, s3_bucket):
    config_path = os.path.expanduser(config)
    ctx.obj = {
        's3_bucket' : s3_bucket
    }

main.add_command(targets)

if __name__ == "__main__":
    main()
