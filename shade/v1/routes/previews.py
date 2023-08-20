# TODO just turn an id into a preview and request preview
import uuid
from io import BytesIO

from PIL import Image
from urllib.parse import quote
from shade.v1.api import API
from shade.v1.types import MountInfo
from pathlib import Path


class Previews:
    def __init__(self, api: API, mount_info: MountInfo):
        self.__api = api
        self.__mount_info = mount_info

    def request_preview(self, path: Path) -> uuid.UUID:
        path = self.__mount_info.translate_filepath_to_server(path)

        response = self.__api.post(f'previews/{quote(str(path))}')

        return uuid.UUID(response.text.strip('"'))

    def get_preview(self, preview_id: uuid.UUID) -> Image:
        response = self.__api.get(f'previews/{preview_id}')

        image_bytes = BytesIO(response.content)

        return Image.open(image_bytes)
