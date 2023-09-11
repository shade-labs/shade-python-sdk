# TODO Lookup asset by path, get all assets, get an asset by id, update an asset's attributes
#  rename maybe?
from shade.v1.api import API
from shade.v1.types import MountInfo
from shade.v1.models import AssetModel
from typing import List


class Assets:
    def __init__(self, api: API, mount_info: MountInfo):
        self.__api = api
        self.__mount_info = mount_info

    def get_all_assets(self) -> List[AssetModel]:
        assets = self.__api.get('assets')

        return [AssetModel(**asset) for asset in assets.json()]
