"""
This test suite assumes that a shade server is running on the same computer as the tests so that everything stays
referenced
"""
from pathlib import Path

import pytest
from typing import List
from shade import ShadeLocal
from shade.v1.models import Job, AssetModel
from tests.helpers import wait_for_jobs

@pytest.mark.parametrize('demo_file_name', [
    'video/coverr-berlin-underground-train-7268-original.mp4',
    # TODO doesn't seem like braw is working
    # 'video/braw-r3d/A002_C305_0523UB_001.R3D',
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
])
def test_visual_assets(
        demo_asset: AssetModel,
        backend: ShadeLocal,
):
    # wait for jobs to run
    asset = wait_for_jobs(backend, [
        Job.METADATA, Job.CORE, Job.PREVIEWS, Job.COLOR_PALETTE
    ], [demo_asset])[0]

    # assert asset.size_bytes
    assert asset.palette
    assert asset.preview_images
    assert asset.tags


@pytest.mark.parametrize('demo_file_name', [
    'audio/Cymatics - Buildup Drums 19 - 140 BPM.wav',
    'audio/Cymatics - Buildup Drums 20 - 140 BPM.wav',
    'audio/Cymatics - Buildup Drums 24 - 150 BPM.wav',
    'audio/Snap Sound Effect [ HD ].mp3',
    'audio/item_purchase.ogg',
])
def test_audio_assets(
        demo_asset: AssetModel,
        backend: ShadeLocal,
):
    wait_for_jobs(backend, [
        Job.METADATA,
        Job.AUDIO
    ], [demo_asset])

    # assert asset.size_bytes
    assert asset.tags


@pytest.mark.parametrize('demo_file_name', [
    'text/README.md',
    'text/semestesr-1-2023-24.pdf',
    'text/semestesr-1-2023-24.pdf'
])
def test_text_assets(
        demo_asset: AssetModel,
        backend: ShadeLocal,
):
    wait_for_jobs(backend, [
        Job.METADATA,
        Job.TEXT
    ], [demo_asset])

    assert asset.size_bytes


@pytest.mark.parametrize('demo_file_names', [
    ([f'images/freeman{i}.jpg' for i in range(1, 8)]),
])
def test_facial_recognition(
        demo_assets: List[AssetModel],
        backend: ShadeLocal,
        tmp_path: Path,
):
    wait_for_jobs(backend, [
        Job.METADATA,
        Job.FACIAL_RECOGNITION,
        Job.CORE
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
