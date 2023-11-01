import os

import pytest

def main():
    # run in test directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    pytest.main()

main()