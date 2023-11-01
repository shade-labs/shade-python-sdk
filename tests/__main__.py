import os

import pytest

# run in test directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

pytest.main()
