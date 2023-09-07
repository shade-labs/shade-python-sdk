# TODO get all assets in a root
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

    def add_new_root(self, path: Path, collection_id: uuid.UUID = None) -> uuid.UUID:
        """
        Add a new root to the index. This will start indexing the root
        """
        resp = self.__api.post('indexing/roots', json={
            'paths': [str(self.__mount_info.translate_filepath_to_server(path))],
            'collection_ids': [str(collection_id)] if collection_id else []
        }).json()

        return uuid.UUID(resp[0])

    def delete_root(self, root_id: uuid.UUID):
        """
        Delete a root from the index. This will stop indexing the root
        """
        self.__api.delete(f'indexing/roots/{root_id}')
