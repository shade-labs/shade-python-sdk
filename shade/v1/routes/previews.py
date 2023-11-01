# TODO just turn an id into a preview and request preview
import uuid
from io import BytesIO
from pathlib import Path

from PIL import Image
from pydantic import BaseModel

from shade.v1.api import API
from shade.v1.types import MountInfo


class Preview(BaseModel):
    id: uuid.UUID
    api: API

    def get_image(self) -> Image:
        response = self.api.get(f'previews/{self.id}')

        image_bytes = BytesIO(response.content)

        return Image.open(image_bytes)

    class Config:
        arbitrary_types_allowed = True


class Previews:
    def __init__(self, api: API, mount_info: MountInfo):
        self.__api = api
        self.__mount_info = mount_info

    def request_preview(self, path: Path) -> Preview:
        path = self.__mount_info.translate_filepath_to_server(path)

        response = self.__api.post(f'previews', params={
            'path': str(path)
        })

        id_ = uuid.UUID(response.json())

        return Preview(
            id=id_,
            api=self.__api
        )

    def get_preview(self, preview_id: uuid.UUID) -> Image:
        return Preview(
            id=preview_id,
            api=self.__api
        ).get_image()
