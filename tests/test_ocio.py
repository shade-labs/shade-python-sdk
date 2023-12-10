from pathlib import Path

import pytest
from PIL import Image

from shade import ShadeLocal


@pytest.mark.parametrize('asset_name', [
    'image/DSC01974.ARW',
    'image/photo-3.jpg',
    'image/exr-hdr-weird/rgba_half.exr',
])
def test_ocio_support(test_assets: Path, backend: ShadeLocal, asset_name: str):
    asset_path = test_assets / asset_name

    assert isinstance(backend.convert.convert_colorspace(asset_path, 'sRGB - Texture', 'ACEScg'), Image.Image)
