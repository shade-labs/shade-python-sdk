import os
import sys

import pytest


def main():
    code = pytest.main(args=[
        os.path.dirname(os.path.abspath(__file__)),
        *sys.argv[1:]  # pass through any arguments
    ])
    sys.exit(code)


if __name__ == '__main__':
    main()
