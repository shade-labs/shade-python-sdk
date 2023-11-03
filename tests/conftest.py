import os
import subprocess
from pathlib import Path

import pytest

from shade import ShadeLocal


@pytest.fixture(scope="session")
def backend() -> ShadeLocal:
    backend = ShadeLocal(port=int(os.getenv('SHADE_PORT', 9082)))
    assert backend.server.status() == 'online'
    return backend


@pytest.fixture(scope="session")
def test_assets(pytestconfig) -> Path:
    data_dir = pytestconfig.cache.mkdir('test_assets')
    print('Synchronizing test assets from GCS (this may take a while)...')
    res = subprocess.run([
        'gsutil',
        'rsync',
        '-r', '-d',
        'gs://shade-test-assets/',
        str(data_dir.resolve())
    ])
    if res.returncode != 0:
        pytest.skip('Failed to download demo assets. Running test suite without them.')

    return data_dir.resolve()
