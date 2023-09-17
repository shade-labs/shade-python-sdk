# TODO Lookup asset by path, get all assets, get an asset by id, update an asset's attributes
#  rename maybe?
import uuid

from shade.v1.api import API
from shade.v1.types import MountInfo
from shade.v1.models import AssetModel
from pathlib import Path
from typing import List


class Assets:
    def __init__(self, api: API, mount_info: MountInfo):
        self.__api = api
        self.__mount_info = mount_info

    def get_all_assets(self) -> List[AssetModel]:
        assets = self.__api.get('assets')

        return [AssetModel(**asset) for asset in assets.json()]

    def get_asset_by_id(self, id_: uuid.UUID) -> AssetModel:
        asset = self.__api.get(f'assets/{id_}')

        return AssetModel(**asset.json())

    def get_asset_by_path(self, path: Path) -> AssetModel:
        asset = self.__api.get(f'indexing/file', params={
            'path': str(path)
        })

        return AssetModel(**asset.json())
