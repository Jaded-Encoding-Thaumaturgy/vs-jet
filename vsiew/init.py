# Shrimply

base_org = 'Irrational-Encoding-Wizardry'


def update(latest_git: bool = False) -> None:
    import sys
    from subprocess import check_call
    from http.client import HTTPSConnection

    def _get_call(package: str, do_git: bool) -> int:
        if do_git:
            package = f'git+https://github.com/{base_org}/{package}.git'

        try:
            return check_call([sys.executable, '-m', 'pip', 'install', package, '-U', '--no-cache-dir'])
        except Exception:
            return 1

    if latest_git:
        err = 0

        conn = HTTPSConnection('raw.githubusercontent.com', 443)
        conn.request('GET', f'https://raw.githubusercontent.com/{base_org}/vs-iew/master/requirements.txt')

        res = conn.getresponse()

        packages = [line.decode('utf-8').strip() for line in res.readlines() if b'#' in line]

        for package in packages:
            *_, package = package.split('# ')

            if _get_call(package, True):
                err += 1

        if err:
            color, message = 31, f'There was an error updating ({err}) IEW packages to latest git!'
        else:
            color, message = 32, 'Successfully updated all IEW packages to latest git!'
    else:
        err = _get_call('vs-iew', True)

        if err:
            err = _get_call('vsiew')

        if err:
            color, message = 31, 'There was an error updating IEW packages!'
        else:
            color, message = 32, 'Successfully updated IEW packages!'

    if sys.stdout and sys.stdout.isatty():
        message = f'\033[0;{color};1m{message}\033[0m'

    print(f'\n\t{message}\n')
