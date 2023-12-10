from pathlib import Path

from PIL import Image
from io import BytesIO
from shade.v1.api import API
from shade.v1.types import MountInfo


class Convert:
    def __init__(self, api: API, mount_info: MountInfo):
        self.__api = api
        self.__mount_info = mount_info

    def convert_colorspace(self, path: Path, in_colorspace: str, out_colorspace: str) -> Image.Image:
        """
        Convert the colorspace of an image
        :param path: The path to the image to convert
        :param in_colorspace: The colorspace to convert from
        :param out_colorspace: The colorspace to convert to
        :return: The converted image
        """
        result = BytesIO(self.__api.post('convert/colorspace', json={
            'file': str(self.__mount_info.translate_filepath_to_server(path)),
            'in_colorspace': in_colorspace,
            'out_colorspace': out_colorspace
        }).content)

        return Image.open(result)
