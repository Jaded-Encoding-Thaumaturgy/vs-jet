import sys
from .init import update


if __name__ == '__main__':
    update(sys.argv and sys.argv[-1] == 'latest')
