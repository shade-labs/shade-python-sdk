import os
import sys

import pytest


def main():
    # run in test directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    code = pytest.main()
    sys.exit(code)


if __name__ == '__main__':
    main()
