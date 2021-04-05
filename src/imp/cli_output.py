import click


def experiment_output(experiment):
    __info(f"ID: {experiment['id']}")
    __info(f"Status: {experiment['state'].get('status')}")
    __info(f"Reason: {experiment['state'].get('reason')}")
    __info(f"Created at: {experiment['creationTime']}")
    __info("")


def __info(text):
    click.echo(text)


def __error(text):
    click.secho(text, fg='red', err=True)
