import uuid
from typing import List, Optional

from shade.v1.api import API
from shade.v1.models import AssetModel
from shade.v1.types import MountInfo


class Server:
    def __init__(self, api: API, mount_info: MountInfo):
        self.__api = api
        self.__mount_info = mount_info

    def status(self) -> str:
        return self.__api.get('status').json()
