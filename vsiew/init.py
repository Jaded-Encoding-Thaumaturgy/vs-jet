# Shrimply

def update() -> None:
    import sys
    from subprocess import check_call

    def _get_call(url: str) -> int:
        try:
            return check_call([sys.executable, '-m', 'pip', 'install', url, '-U', '--no-cache-dir'])
        except Exception:
            return 1

    err = _get_call('git+https://github.com/Irrational-Encoding-Wizardry/vs-iew.git')

    if err:
        err = _get_call('vsiew')

    if err:
        color, message = 31, 'There was an error updating IEW packages!'
    else:
        color, message = 32, 'Successfully updated IEW packages!'

    if sys.stdout and sys.stdout.isatty():
        message = f'\033[0;{color};1m{message}\033[0m'

    print(f'\n\t{message}\n')
