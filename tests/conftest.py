import os
from pathlib import Path
from typing import List

import pytest
from google.cloud import storage
from shade import ShadeLocal
from shade.v1.models import AssetModel, RootModel
from tests.helpers import wait_for_assets


@pytest.fixture(scope="session")
def backend() -> ShadeLocal:
    backend = ShadeLocal(port=int(os.getenv('SHADE_PORT', 9082)))
    assert backend.server.status() == 'online'

    # backend.models.enable_all_models()
    backend.models.enable_model('blip')
    backend.models.enable_model('audio')
    backend.models.enable_model('text')
    backend.models.enable_model('braw')

    return backend


@pytest.fixture
def demo_file_path(pytestconfig, demo_file_name: str, tmp_path) -> Path:
    """
    Fixture to request path to test asset.

    :param demo_file_name: name of the asset.
    """
    cache_dir = pytestconfig.cache.mkdir("demo_assets")
    asset_path = cache_dir / demo_file_name
    # TODO check for changes in the remote asset
    if not asset_path.exists():
        print(
            f"downloading demo asset {demo_file_name} because it was not found in the cache"
        )
        storage_client = storage.Client.create_anonymous_client()
        bucket = storage_client.bucket("shade-test-assets")
        blob = bucket.blob(demo_file_name)
        asset_path.parent.mkdir(parents=True, exist_ok=True)
        blob.download_to_filename(str(asset_path))

    # copy it somewhere safe, in case the test modifies it
    tmp_asset_path = tmp_path / demo_file_name
    tmp_asset_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_asset_path.write_bytes(asset_path.read_bytes())
    yield tmp_asset_path
    tmp_asset_path.unlink(missing_ok=True)


@pytest.fixture
def demo_file_paths(pytestconfig, demo_file_names: List[str], tmp_path) -> List[Path]:
    """
    Fixture to request a bunch of paths for a test.

    :param demo_file_names: name of the asset.
    """
    cache_dir = pytestconfig.cache.mkdir("demo_assets")

    demo_file_paths = []
    for demo_file_name in demo_file_names:
        asset_path = cache_dir / demo_file_name
        # TODO check for changes in the remote asset
        if not asset_path.exists():
            print(
                f"downloading demo asset {demo_file_name} because it was not found in the cache"
            )
            storage_client = storage.Client.create_anonymous_client()
            bucket = storage_client.bucket("shade-test-assets")
            blob = bucket.blob(demo_file_name)
            asset_path.parent.mkdir(parents=True, exist_ok=True)
            blob.download_to_filename(str(asset_path))

        # copy it somewhere safe, in case the test modifies it
        tmp_asset_path = tmp_path / 'demo_assets' / demo_file_name
        tmp_asset_path.parent.mkdir(parents=True, exist_ok=True)
        tmp_asset_path.write_bytes(asset_path.read_bytes())

        demo_file_paths.append(tmp_asset_path)

    yield demo_file_paths

    for tmp_asset_path in demo_file_paths:
        tmp_asset_path.unlink(missing_ok=True)


@pytest.fixture
def demo_asset_root(backend: ShadeLocal, tmp_path: Path) -> RootModel:
    root_path = tmp_path / 'asset_root'
    root_path.mkdir(parents=True, exist_ok=True)
    root_id = backend.roots.add_new_root(root_path)

    try:
        # TODO there's a route to get root by id somewhere...
        roots = backend.roots.get_roots()
        root = next((root for root in roots if root.id == root_id), None)
        assert root, f"Root was not found: {root_id}"
        yield root
    finally:
        # TODO could delete the folder too?
        backend.roots.delete_root(root_id)


@pytest.fixture
def demo_asset(backend: ShadeLocal, demo_file_path: Path, demo_asset_root: RootModel) -> AssetModel:
    asset_path = Path(demo_asset_root.local_path) / demo_file_path.name
    demo_file_path.rename(asset_path)

    backend.indexing.resync()
    return wait_for_assets(backend, [asset_path])[0]


@pytest.fixture
def demo_assets(backend: ShadeLocal, demo_file_paths: Path, demo_asset_root: Path) -> AssetModel:
    root_path = Path(demo_asset_root.local_path)
    asset_paths = [root_path / demo_file_path.name for demo_file_path in demo_file_paths]
    for demo_file_path, asset_path in zip(demo_file_paths, asset_paths):
        demo_file_path.rename(asset_path)

    backend.indexing.resync()
    return wait_for_assets(backend, asset_paths, timeout=500)[0]
