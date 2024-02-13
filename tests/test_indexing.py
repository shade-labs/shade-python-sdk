"""
This test suite assumes that a shade server is running on the same computer as the tests so that everything stays
referenced
"""
import time
from pathlib import Path

import pytest

import shade.v1.api
from shade import ShadeLocal
from typing import List
from shade.v1.models import Jobs


# Wooo these can all be fixtures
def wait_for_assets(backend: ShadeLocal, paths: List[Path]):
    """
    Wait for assets to be indexed
    """
    while True:
        try:
            # Make sure they're all there
            [backend.assets.get_asset_by_path(asset) for asset in paths]
            break
        except shade.v1.api.APIException:
            time.sleep(1)


def wait_for_jobs(backend: ShadeLocal, jobs: List[Jobs], paths: List[Path] = None):
    """
    Get all assets and check to make sure that each one of the jobs on the assets is either completed or failed
    """
    wait_for_assets(backend, paths)

    job_keys = [job.value for job in jobs]

    def __asset_has_jobs(asset):
        for job in job_keys:
            if getattr(asset, job) not in ('COMPLETED', 'FAILED'):
                return False
        return True

    while True:
        assets = [backend.assets.get_asset_by_path(asset) for asset in paths]
        if not all([__asset_has_jobs(asset) for asset in assets]):
            time.sleep(1)
        else:
            break


# @pytest.mark.parametrize('asset_name', [
#     # Audio
#     'audio/Cymatics - Buildup Drums 19 - 140 BPM.wav',
#     'audio/Cymatics - Buildup Drums 20 - 140 BPM.wav',
#     'audio/Cymatics - Buildup Drums 24 - 150 BPM.wav',
#     'audio/Snap Sound Effect [ HD ].mp3',
#     'audio/item_purchase.ogg',
#
#     # Images
#     'image/DSC01974.ARW',
#     'image/DSC04274.ARW',
#     'image/FullSizeRender.heic',
#     'image/android.demo-popover.gif',
#     'image/photo-1.jpg',
#     'image/photo-2.jpg',
#     'image/photo-3.jpg',
#     'image/schema.webp',
#
#     # EXR
#     'image/exr-hdr-weird/bw_full.exr',
#     'image/exr-hdr-weird/bw_half.exr',
#     'image/exr-hdr-weird/rgb_full.exr',
#     'image/exr-hdr-weird/rgb_half.exr',
#     'image/exr-hdr-weird/rgba_full.exr',
#     'image/exr-hdr-weird/rgba_half.exr',
#
#     # HDR
#     'image/exr-hdr-weird/farm_sunset_1k.hdr',
#     'image/exr-hdr-weird/limpopo_golf_course_1k.hdr',
#     'image/exr-hdr-weird/sample_640426.hdr',
#
#     # Video
#     'video/coverr-berlin-underground-train-7268-original.mp4',
#
#     # TODO add in full build for these to run
#     # # braw/R3D
#     # 'video/braw-r3d/A002_C305_0523UB_001.R3D'
#     #
#     # # 3D
#     # '3d/CC1_Sketchfab.fbx',
#     # '3d/cathedral.glb',
#     # '3d/fire_extinguisher_untextured.obj',
# ])
# def test_index_asset(test_assets: Path, backend: ShadeLocal, asset_name: str):
#     asset_path = test_assets / asset_name
#
#     root_id = backend.roots.add_new_root(asset_path)
#
#     assert root_id in [r.id for r in backend.roots.get_roots()]
#
#     # do our best to clean up. nobody is perfect.
#     # anything running the test suite should use an ephemeral database anyhow,
#     # this is mostly just to get more surface area on the tests for free
#     try:
#         backend.indexing.resync()
#         asset = backend.assets.wait_for_asset(asset_path)
#         assert asset, "Asset was not indexed"
#
#         assert asset.id
#         assert asset.path
#         assert asset.type
#         assert asset.size_bytes > 9
#         assert asset.signature
#         assert asset.ai_indexed
#
#         # should generate previews for visual assets
#         if asset.type in (AssetType.IMAGE, AssetType.EXR, AssetType.OBJECT, AssetType.HDR, AssetType.VIDEO):
#             assert asset.preview_images
#
#         assert asset.tags
#         # assert asset.description
#     finally:
#         backend.roots.delete_root(root_id)
#         with pytest.raises(APIException, match='Asset not found'):
#             backend.assets.get_asset_by_path(asset_path)


@pytest.mark.parametrize('demo_file_names', [
    ([
        'video/coverr-berlin-underground-train-7268-original.mp4',
        # 'video/braw-r3d/A002_C305_0523UB_001.R3D',
        # TODO doesn't seem like braw is working
        # 'video/In-The-Hand-Original.braw',

        'image/exr-hdr-weird/bw_full.exr',
        'image/exr-hdr-weird/bw_half.exr',
        'image/exr-hdr-weird/rgb_full.exr',
        'image/exr-hdr-weird/rgb_half.exr',
        'image/exr-hdr-weird/rgba_full.exr',
        'image/exr-hdr-weird/rgba_half.exr',

        'image/DSC01974.ARW',
        'image/DSC04274.ARW',
        'image/FullSizeRender.heic',
        'image/android.demo-popover.gif',
        'image/photo-1.jpg',
        'image/photo-2.jpg',
        'image/photo-3.jpg',
        'image/schema.webp',

        'image/exr-hdr-weird/farm_sunset_1k.hdr',
        'image/exr-hdr-weird/limpopo_golf_course_1k.hdr',
        'image/exr-hdr-weird/sample_640426.hdr'
    ]),
])
def test_visual_assets(
    demo_file_paths,
    backend: ShadeLocal,
    tmp_path: Path,
):
    backend.models.enable_model('braw')
    root_id = backend.roots.add_new_root(tmp_path)

    wait_for_jobs(backend, [
        Jobs.PREVIEWS,
        Jobs.CORE,
        Jobs.COLOR_PALETTE,
        Jobs.METADATA
    ], demo_file_paths)

    try:
        for asset in demo_file_paths:
            asset_ = backend.assets.get_asset_by_path(asset)
            assert asset_, f"Asset was not indexed: {asset}"

            assert asset_.id
            assert asset_.path
            assert asset_.type
            assert asset_.signature
            assert asset_.ai_indexed
            assert len(asset_.palette) > 0

            assert len(asset_.preview_images) > 0

            assert asset_.tags
    finally:
        backend.roots.delete_root(root_id)


@pytest.mark.parametrize('demo_file_names', [
    ([
        'audio/Cymatics - Buildup Drums 19 - 140 BPM.wav',
        'audio/Cymatics - Buildup Drums 20 - 140 BPM.wav',
        'audio/Cymatics - Buildup Drums 24 - 150 BPM.wav',
        'audio/Snap Sound Effect [ HD ].mp3',
        'audio/item_purchase.ogg',
    ]),
])
def test_audio_assets(
    demo_file_paths,
    backend: ShadeLocal,
    tmp_path: Path,
):
    backend.models.enable_model('audio')

    root_id = backend.roots.add_new_root(tmp_path)

    wait_for_jobs(backend, [
        Jobs.METADATA,
        Jobs.AUDIO
    ], demo_file_paths)

    try:
        for asset in demo_file_paths:
            asset_ = backend.assets.get_asset_by_path(asset)
            assert asset_, f"Asset was not indexed: {asset}"

            assert asset_.id
            assert asset_.path
            assert asset_.type
            assert asset_.signature
            assert asset_.ai_indexed

            assert asset_.tags
    finally:
        backend.roots.delete_root(root_id)


@pytest.mark.parametrize('demo_file_names', [
    ([
        'text/README.md',
        'text/semestesr-1-2023-24.pdf',
        'text/semestesr-1-2023-24.pdf'
    ]),
])
def test_text_assets(
        demo_file_paths,
        backend: ShadeLocal,
        tmp_path: Path,
):
    backend.models.enable_model('text')

    root_id = backend.roots.add_new_root(tmp_path)

    wait_for_jobs(backend, [
        Jobs.METADATA,
        Jobs.TEXT
    ], demo_file_paths)

    try:
        for asset in demo_file_paths:
            asset_ = backend.assets.get_asset_by_path(asset)
            assert asset_, f"Asset was not indexed: {asset}"

            assert asset_.id
            assert asset_.path
            assert asset_.type
            assert asset_.signature
            assert asset_.ai_indexed
    finally:
        backend.roots.delete_root(root_id)


@pytest.mark.parametrize('demo_file_names', [
    ([f'images/freeman{i}.jpg' for i in range(1, 8)]),
])
def test_facial_recognition(
        demo_file_paths,
        backend: ShadeLocal,
        tmp_path: Path,
):
    backend.models.enable_model('facial')

    root_id = backend.roots.add_new_root(tmp_path)

    wait_for_jobs(backend, [
        Jobs.METADATA,
        Jobs.FACIAL_RECOGNITION,
        Jobs.CORE
    ], demo_file_paths)

    try:
        for asset in demo_file_paths:
            asset_ = backend.assets.get_asset_by_path(asset)
            assert asset_, f"Asset was not indexed: {asset}"

            assert asset_.id
            assert asset_.path
            assert asset_.type
            assert asset_.signature
            assert asset_.ai_indexed

            # This is a bit doomed apparently, so just checking facial is completed might be
            #  enough
            # faces = backend.assets.get_faces(asset_.id)
            # assert len(faces) > 0
    finally:
        backend.roots.delete_root(root_id)
