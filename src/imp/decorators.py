import click


def handle_exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            click.secho(f'{type(e).__name__}: {e}', fg='red', err=True)
    return wrapper
