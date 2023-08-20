import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

from shade.v1.api import API
from shade.v1.types import ServerResponse, MountInfo
from typing import List


class RootModel(ServerResponse):
    id: uuid.UUID
    created: datetime
    updated: datetime
    files_found: int = 0
    size_bytes: int = 0

    is_directory: bool

    ctime: Optional[datetime] = None
    mtime: Optional[datetime] = None


class Roots:
    def __init__(self, api: API, mount_info: MountInfo):
        self.__api = api
        self.__mount_info = mount_info

    def get_roots(self) -> List[RootModel]:
        """
        Get all roots from the API. Roots are the top level directories that
        shade is indexing / searching from
        """
        return [RootModel(**root, mount_info=self.__mount_info) for root in self.__api.get('indexing/roots').json()]
