from cli_output import cli_error


def handle_exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            cli_error(f'{type(e).__name__}: {e}')
    return wrapper
