"""
This test suite assumes that a shade server is running on the same computer as the tests so that everything stays
referenced
"""
from pathlib import Path
from typing import List
from urllib.parse import unquote

import requests

from shade import ShadeLocal
from shade.v1.models import AssetType


def pytest_configure(config):
    # Don't capture output
    config.option.capture = "no"


assets = [
    # Audio
    'https://storage.googleapis.com/shade-test-assets/audio/Cymatics%20-%20Buildup%20Drums%2019%20-%20140%20BPM.wav',
    'https://storage.googleapis.com/shade-test-assets/audio/Cymatics%20-%20Buildup%20Drums%2020%20-%20140%20BPM.wav',
    'https://storage.googleapis.com/shade-test-assets/audio/Cymatics%20-%20Buildup%20Drums%2024%20-%20150%20BPM.wav',
    'https://storage.googleapis.com/shade-test-assets/audio/Snap%20Sound%20Effect%20%5B%20HD%20%5D.mp3',
    'https://storage.googleapis.com/shade-test-assets/audio/item_purchase.ogg',

    # 3D (doesn't work because no frontend)
    'https://storage.googleapis.com/shade-test-assets/3d/CC1_Sketchfab.fbx',
    'https://storage.googleapis.com/shade-test-assets/3d/cathedral.glb',
    'https://storage.googleapis.com/shade-test-assets/3d/fire_extinguisher_untextured.obj',

    # Images
    'https://storage.googleapis.com/shade-test-assets/image/DSC01974.ARW',
    'https://storage.googleapis.com/shade-test-assets/image/DSC04274.ARW',
    'https://storage.googleapis.com/shade-test-assets/image/FullSizeRender.heic',
    'https://storage.googleapis.com/shade-test-assets/image/android.demo-popover.gif',
    'https://storage.googleapis.com/shade-test-assets/image/photo-1685361063181-1d0471c063a9%3Fcrop%3Dentropy%26cs%3Dtinysrgb%26fit%3Dcrop%26fm%3Djpg%26h%3D1130%26ixid%3DMnwxfDB8MXxyYW5kb218MHx8fHx8fHx8MTY4Njg4ODQ3Ng%26ixlib%3Drb-4.0.3%26q%3D80%26utm_campaign%3Dapi-credit%26utm_medium%3Dreferral%26utm_source%3Dunsplash_source%26w%3D1920.jpg',
    'https://storage.googleapis.com/shade-test-assets/image/photo-1686466444490-19b4d3a0aba2%3Fcrop%3Dentropy%26cs%3Dtinysrgb%26fit%3Dcrop%26fm%3Djpg%26h%3D1095%26ixid%3DMnwxfDB8MXxyYW5kb218MHx8fHx8fHx8MTY4Njg4ODIzMw%26ixlib%3Drb-4.0.3%26q%3D80%26utm_campaign%3Dapi-credit%26utm_medium%3Dreferral%26utm_source%3Dunsplash_source%26w%3D1920.jpg',
    'https://storage.googleapis.com/shade-test-assets/image/photo-1686610620643-0ba20d31b6f5%3Fcrop%3Dentropy%26cs%3Dtinysrgb%26fit%3Dcrop%26fm%3Djpg%26h%3D1120%26ixid%3DMnwxfDB8MXxyYW5kb218MHx8fHx8fHx8MTY4Njg4ODI2Mg%26ixlib%3Drb-4.0.3%26q%3D80%26utm_campaign%3Dapi-credit%26utm_medium%3Dreferral%26utm_source%3Dunsplash_source%26w%3D1920.jpg',
    'https://storage.googleapis.com/shade-test-assets/image/schema.webp',

    # EXR
    'https://storage.googleapis.com/shade-test-assets/image/exr-hdr-weird/bw_full.exr',
    'https://storage.googleapis.com/shade-test-assets/image/exr-hdr-weird/bw_half.exr',
    'https://storage.googleapis.com/shade-test-assets/image/exr-hdr-weird/rgb_full.exr',
    'https://storage.googleapis.com/shade-test-assets/image/exr-hdr-weird/rgb_half.exr',
    'https://storage.googleapis.com/shade-test-assets/image/exr-hdr-weird/rgba_full.exr',
    'https://storage.googleapis.com/shade-test-assets/image/exr-hdr-weird/rgba_half.exr',

    # HDR
    'https://storage.googleapis.com/shade-test-assets/image/exr-hdr-weird/farm_sunset_1k.hdr',
    'https://storage.googleapis.com/shade-test-assets/image/exr-hdr-weird/limpopo_golf_course_1k.hdr',
    'https://storage.googleapis.com/shade-test-assets/image/exr-hdr-weird/sample_640426.hdr',

    # Video
    'https://storage.googleapis.com/shade-test-assets/video/coverr-berlin-underground-train-7268-original.mp4',

    # R3D
    'https://storage.googleapis.com/shade-test-assets/video/braw-r3d/A002_C305_0523UB_001.R3D'

    # TODO braw
]


def download_file(url: str, folder: Path) -> Path:
    """
    Download the file from the URL and place it with the proper ending into the given folder, then return the asset path
    """
    response = requests.get(url, stream=True)
    response.raise_for_status()

    # Get the filename from the url
    filename = unquote(url.split('/')[-1])
    # Create the asset path
    asset_path = folder / filename

    if asset_path.exists():
        return asset_path

    # Write the file
    with asset_path.open('wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    return asset_path


def download_files(urls: List[str]) -> List[Path]:
    """
    Download all of the files from the given list of urls
    """
    # Make the data dir if it doesn't exist
    download_folder = Path('./data').resolve()
    download_folder.mkdir(parents=True, exist_ok=True)
    download_paths = []
    for url in urls:
        print(f"Downloading: {url}")
        download_paths.append(download_file(url, download_folder))

    return download_paths


def test_indexing():
    """
    Megatest to just download all the files, then add the root, then assert the document for each one depending on type
    """
    global assets
    download_paths = download_files(assets)

    backend = ShadeLocal()

    try:
        backend.roots.add_new_root(Path('./data').resolve())

        backend.indexing.resync()
    except Exception as e:
        print(f"Small issue: {e}")

    # Now wait for indexing to finish
    backend.indexing.wait_for_indexing()

    # Now assert that all the files are indexed
    for path in download_paths:
        # They should all get indexed!
        print(f"Getting asset at {path}")
        asset = backend.assets.get_asset_by_path(path)
        # Now basically just assert that the asset is correct
        assert asset.id is not None
        assert asset.path is not None
        assert asset.type is not None
        assert asset.size_bytes > 9
        assert asset.signature
        assert asset.ai_indexed

        if asset.type == AssetType.AUDIO:
            assert asset.description
            assert asset.tags
        elif asset.type in (AssetType.IMAGE, AssetType.EXR, AssetType.OBJECT, AssetType.HDR, AssetType.VIDEO):
            assert asset.preview_images
            assert asset.tags
            assert asset.description

    data_folder = download_paths[0].parent
    files = backend.search.list_assets_in_folder(data_folder)

    print(len(files))
    print(files)

    assert len(files) == len(list(data_folder.iterdir()))
