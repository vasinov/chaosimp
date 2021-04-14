import click

from src.name_constants import *


def automation_output(automation: dict) -> None:
    if automation:
        cli_info("Automation")
        cli_info("")


def template_output(template: dict) -> None:
    if template:
        name = next((t["Value"] for t in template['Tags'] if t['Key'] == TAG_KEY_ORIGINAL_NAME), {})

        cli_info(f"Cloud Formation ID: {template['StackId']}")
        cli_info(f"Name: {name}")
        cli_info(f"Status: {template['StackStatus']}")
        cli_info(f"Created at: {template['CreationTime']}")
        cli_info("")


def experiment_output(experiment: dict) -> None:
    if experiment:
        cli_info(f"ID: {experiment['id']}")
        cli_info(f"Name: {experiment['tags'].get(TAG_KEY_ORIGINAL_NAME, '')}")
        cli_info(f"Status: {experiment['state'].get('status')}")
        cli_info(f"Reason: {experiment['state'].get('reason')}")
        cli_info(f"Created at: {experiment['creationTime']}")
        cli_info("")


def cli_info(text: str) -> None:
    click.echo(text)


def cli_success(text: str) -> None:
    click.secho(text, fg='green')


def cli_warn(text: str) -> None:
    click.secho(text, fg='yellow')


def cli_error(text: str) -> None:
    click.secho(text, fg='red', err=True)
