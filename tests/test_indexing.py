"""
This test suite assumes that a shade server is running on the same computer as the tests so that everything stays
referenced
"""
from pathlib import Path

import pytest

from shade import ShadeLocal
from shade.v1.models import AssetType


@pytest.mark.parametrize('asset_name', [
    # Audio
    'audio/Cymatics%20-%20Buildup%20Drums%2019%20-%20140%20BPM.wav',
    'audio/Cymatics%20-%20Buildup%20Drums%2020%20-%20140%20BPM.wav',
    'audio/Cymatics%20-%20Buildup%20Drums%2024%20-%20150%20BPM.wav',
    'audio/Snap%20Sound%20Effect%20%5B%20HD%20%5D.mp3',
    'audio/item_purchase.ogg',

    # 3D
    '3d/CC1_Sketchfab.fbx',
    '3d/cathedral.glb',
    '3d/fire_extinguisher_untextured.obj',

    # Images
    'image/DSC01974.ARW',
    'image/DSC04274.ARW',
    'image/FullSizeRender.heic',
    'image/android.demo-popover.gif',
    'image/photo-1685361063181-1d0471c063a9%3Fcrop%3Dentropy%26cs%3Dtinysrgb%26fit%3Dcrop%26fm%3Djpg%26h%3D1130%26ixid%3DMnwxfDB8MXxyYW5kb218MHx8fHx8fHx8MTY4Njg4ODQ3Ng%26ixlib%3Drb-4.0.3%26q%3D80%26utm_campaign%3Dapi-credit%26utm_medium%3Dreferral%26utm_source%3Dunsplash_source%26w%3D1920.jpg',
    'image/photo-1686466444490-19b4d3a0aba2%3Fcrop%3Dentropy%26cs%3Dtinysrgb%26fit%3Dcrop%26fm%3Djpg%26h%3D1095%26ixid%3DMnwxfDB8MXxyYW5kb218MHx8fHx8fHx8MTY4Njg4ODIzMw%26ixlib%3Drb-4.0.3%26q%3D80%26utm_campaign%3Dapi-credit%26utm_medium%3Dreferral%26utm_source%3Dunsplash_source%26w%3D1920.jpg',
    'image/photo-1686610620643-0ba20d31b6f5%3Fcrop%3Dentropy%26cs%3Dtinysrgb%26fit%3Dcrop%26fm%3Djpg%26h%3D1120%26ixid%3DMnwxfDB8MXxyYW5kb218MHx8fHx8fHx8MTY4Njg4ODI2Mg%26ixlib%3Drb-4.0.3%26q%3D80%26utm_campaign%3Dapi-credit%26utm_medium%3Dreferral%26utm_source%3Dunsplash_source%26w%3D1920.jpg',
    'image/schema.webp',

    # EXR
    'image/exr-hdr-weird/bw_full.exr',
    'image/exr-hdr-weird/bw_half.exr',
    'image/exr-hdr-weird/rgb_full.exr',
    'image/exr-hdr-weird/rgb_half.exr',
    'image/exr-hdr-weird/rgba_full.exr',
    'image/exr-hdr-weird/rgba_half.exr',

    # HDR
    'image/exr-hdr-weird/farm_sunset_1k.hdr',
    'image/exr-hdr-weird/limpopo_golf_course_1k.hdr',
    'image/exr-hdr-weird/sample_640426.hdr',

    # Video
    'video/coverr-berlin-underground-train-7268-original.mp4',

    # braw/R3D
    'video/braw-r3d/A002_C305_0523UB_001.R3D'
])
def test_index_asset(test_assets: Path, backend: ShadeLocal, asset_name: str):
    asset_path = test_assets / asset_name

    backend.roots.add_new_root(asset_path)

    # do our best to clean up. nobody is perfect.
    # anything running the test suite should use an ephemeral database anyhow,
    # this is mostly just to get more surface area on the tests for free
    try:
        backend.indexing.resync()
        backend.indexing.wait_for_indexing()

        asset = backend.assets.get_asset_by_path(asset_path)
        assert asset, "Asset was not indexed"

        assert asset.id
        assert asset.path
        assert asset.type
        assert asset.size_bytes > 9
        assert asset.signature
        assert asset.ai_indexed

        # should generate previews for visual assets
        if asset.type in (AssetType.IMAGE, AssetType.EXR, AssetType.OBJECT, AssetType.HDR, AssetType.VIDEO):
            assert asset.preview_images

        assert asset.tags
        assert asset.description
    finally:
        backend.roots.delete_root(asset_path)
        asset = backend.assets.get_asset_by_path(asset_path)
        assert not asset, "Asset was not deleted when root was removed"

