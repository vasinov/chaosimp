import click

from lib.clients.s3 import S3

@click.group()
@click.pass_context
def targets(ctx):
    pass

@targets.command()
@click.pass_context
def list(ctx):
     s3 = S3()

     s3.list(ctx.obj['s3_bucket'], 'targets')
