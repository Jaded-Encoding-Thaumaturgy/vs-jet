from .init import update

# python -m vsstg
if __name__ == '__main__':
    import sys
    update(sys.argv[1:])
