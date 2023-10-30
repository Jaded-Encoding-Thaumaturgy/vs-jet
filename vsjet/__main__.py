from .init import update

# python -m vsjet
if __name__ == '__main__':
    import sys
    update(sys.argv[1:])
