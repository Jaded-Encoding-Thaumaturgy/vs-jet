# Shrimply

base_user = 'Jaded-Encoding-Thaumaturgy'


def update(action_: list[str] | None) -> None:
    import re
    import sys
    from shutil import which
    from subprocess import PIPE, Popen
    from typing import Iterator

    if not which('git'):
        raise ImportError('Git is not installed! Please install git before you continue.')

    action = 'update'

    if action_:
        if action_[-1] == 'latest':
            action = 'update-git'
        elif 'Scripts' not in action_[-1] or '.py' not in action_[-1]:
            action = action_[-1].strip()

    def _get_install_call(package: str, do_git: bool) -> int:
        from subprocess import check_call

        args = list[str]()

        if do_git:
            github_path = package if '/' in package else f'{base_user}/{package}'
            package = f'git+https://github.com/{github_path}.git'
            args.extend(['--force', '--no-deps', '--use-pep517'])
        elif '/' in package:
            return 0

        try:
            return check_call([
                sys.executable, '-m', 'pip', 'install',
                package, '-U', '--no-cache-dir', *args
            ])
        except Exception:
            return 1

    def _get_uninstall_call(package: str) -> int:
        from subprocess import check_call

        try:
            return check_call([
                sys.executable, '-m', 'pip', 'uninstall', package, '-y'
            ])
        except Exception:
            return 1

    def _get_jet_packages() -> Iterator[tuple[str, str]]:
        from urllib.request import urlopen

        res = urlopen(f'https://raw.githubusercontent.com/{base_user}/vs-jet/master/requirements.txt')

        for line in res.readlines():
            if b'#' in line:
                line_s = line.decode('utf-8').strip()

                package, _, pypi_package = line_s.partition('# ')
                package = package.split('=')[0].strip('<>')

                yield (package, pypi_package)

    def _fix_own_dependencies() -> int:
        err = 0

        process = Popen([sys.executable, '-m', 'pip', 'check'], encoding='utf8', stdout=PIPE)
        process.wait()

        if not process.stdout:
            return err

        regex = re.compile(r"(.+)\s[\d.]+\shas requirement\s(.+),")

        deps_to_fix = set[str]()

        for package_err in process.stdout.readlines():
            package_match = regex.match(package_err)

            if not package_match:
                continue

            pack_err, pack_good = package_match[1], package_match[2]

            for (package, _) in packages:
                if package.lower() == pack_err.lower():
                    break
            else:
                continue

            deps_to_fix.add(pack_good)

        for dep in deps_to_fix:
            if _get_install_call(dep, False):
                err += 1

        return err

    err = deps_err = color = 0
    message = default_message = 'No error message specified'

    def _set_message(
        message_succ: str = default_message, message_err: str = default_message
    ) -> None:
        nonlocal color, message, err
        color = 31 if err else 32
        message = (message_err if err else message_succ).format(err=err)
        if deps_err:
            message += f'\n\tThere were {deps_err} errors installing dependencies! Run `pip check` for more info.'

    if action == 'update':
        packages = list(_get_jet_packages())
        for name, _ in reversed(packages):
            _get_uninstall_call(name)

        for name, _ in packages:
            if _get_install_call(name, False):
                err += 1

        _set_message(
            'Successfully updated all packages!',
            'There was an error updating all packages!'
        )
    elif action == 'update-git':
        packages = list(_get_jet_packages())
        for name, _ in reversed(packages):
            _get_uninstall_call(name)

        for _, repo_name in packages:
            if _get_install_call(repo_name, True):
                err += 1

        deps_err = _fix_own_dependencies()

        _set_message(
            'Successfully updated all packages to latest git!',
            'There was an error updating ({err}) packages to latest git!'
        )
    elif action == 'uninstall':
        for name, _ in reversed(list(_get_jet_packages())):
            if _get_uninstall_call(name):
                err += 1

        _set_message(
            'Successfully uninstalled all packages!',
            'There was an error uninstalling ({err}) packages!'
        )
    else:
        err = 1
        _set_message(message_err=f'There\'s no action called "{action}"!')

    if sys.stdout and sys.stdout.isatty():
        message = f'\033[0;{color};1m{message}\033[0m'

    print(f'\n\t{message}\n')
