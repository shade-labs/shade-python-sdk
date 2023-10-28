# TODO big search query + filters, similar assets
import uuid
from typing import List, Optional

from shade.v1.api import API
from shade.v1.models import AssetModel
from shade.v1.types import MountInfo
from pathlib import Path


class Search:
    def __init__(self, api: API, mount_info: MountInfo):
        self.__api = api
        self.__mount_info = mount_info

    def search(self,
               query: str = None,
               collection_ids=None,
               file_types=None,
               file_extensions=None,
               tags=None,
               limit: int = 100,
               page: int = 0,
               folder: Optional[str] = None,
               recursive: bool = False,
               filter_ai: bool = False,
               categories=None,
               date_added=None,
               sort: Optional[str] = None,
               exclude_file_types=None,
               ) -> List[AssetModel]:
        # TODO there are a few more filters that I'm leaving out here
        if exclude_file_types is None:
            exclude_file_types = []
        if date_added is None:
            date_added = []
        if categories is None:
            categories = []
        if tags is None:
            tags = []
        if file_extensions is None:
            file_extensions = []
        if file_types is None:
            file_types = []
        if collection_ids is None:
            collection_ids = []

        return [AssetModel(**asset, mount_info=self.__mount_info) for asset in self.__api.get('search', params={
            'query': query,
            'collection_ids': collection_ids,
            'file_types': file_types,
            'file_extensions': file_extensions,
            'tags': tags,
            'limit': limit,
            'page': page,
            'folder': folder,
            'recursive': recursive,
            'filter_ai': filter_ai,
            'categories': categories,
            'date_added': date_added,
            'sort': sort,
            'exclude_file_types': exclude_file_types,
        }).json()]

    def similar(self, asset_id: uuid.UUID):
        return [AssetModel(**asset, mount_info=self.__mount_info) for asset in
                self.__api.get(f'assets/{asset_id}/similar').json()]

    def list_assets_in_folder(self, path: Path, recursive=False) -> List[AssetModel]:
        return self.search(folder=path,
                           recursive=recursive)
