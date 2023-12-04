"""
This test suite assumes that a shade server is running on the same computer as the tests so that everything stays
referenced
"""
from pathlib import Path

import pytest

from shade import ShadeLocal
from shade.v1.models import AssetType
from shade.v1.api import APIException


@pytest.mark.parametrize('asset_name', [
    # Audio
    'audio/Cymatics - Buildup Drums 19 - 140 BPM.wav',
    'audio/Cymatics - Buildup Drums 20 - 140 BPM.wav',
    'audio/Cymatics - Buildup Drums 24 - 150 BPM.wav',
    'audio/Snap Sound Effect [ HD ].mp3',
    'audio/item_purchase.ogg',

    # Images
    'image/DSC01974.ARW',
    'image/DSC04274.ARW',
    'image/FullSizeRender.heic',
    'image/android.demo-popover.gif',
    'image/photo-1.jpg',
    'image/photo-2.jpg',
    'image/photo-3.jpg',
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

    # TODO add in full build for these to run
    # # braw/R3D
    # 'video/braw-r3d/A002_C305_0523UB_001.R3D'
    #
    # # 3D
    # '3d/CC1_Sketchfab.fbx',
    # '3d/cathedral.glb',
    # '3d/fire_extinguisher_untextured.obj',
])
def test_index_asset(test_assets: Path, backend: ShadeLocal, asset_name: str):
    asset_path = test_assets / asset_name

    root_id = backend.roots.add_new_root(asset_path)

    # do our best to clean up. nobody is perfect.
    # anything running the test suite should use an ephemeral database anyhow,
    # this is mostly just to get more surface area on the tests for free
    try:
        backend.indexing.resync()
        asset = backend.assets.wait_for_asset(asset_path)
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
        backend.roots.delete_root(root_id)
        with pytest.raises(APIException, match='Asset not found'):
            backend.assets.get_asset_by_path(asset_path)
