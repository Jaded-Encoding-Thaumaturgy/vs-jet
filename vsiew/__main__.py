import sys

from .init import update

if __name__ == '__main__':
    action = 'update'

    if sys.argv:
        if sys.argv[-1] == 'latest':
            action = 'update-git'
        else:
            action = sys.argv[-1].strip()

    update(action)
