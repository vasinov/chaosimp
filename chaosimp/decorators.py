from types import LambdaType

from chaosimp.cli_output import cli_error


def handle_exception(func: LambdaType):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            cli_error(f'{type(e).__name__}: {e}')
    return wrapper
