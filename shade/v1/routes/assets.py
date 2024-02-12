import time
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
        """
        TODO handle translation (or not)
        Get an asset by its path

        :param path: The path to the asset
        :return: The asset
        """
        asset = self.__api.get(f'indexing/file', params={
            'path': str(path)
        })

        return AssetModel(**asset.json())

    def update_asset(self,
                     id_: uuid.UUID,
                     description: str = None,
                     rating: int = None,
                     category: str = None,
                     tags: list = None,
                     path: Path = None) -> None:
        """
        Update an asset's attributes
        :param id_: The id of the asset to update
        :param description: The new description
        :param rating: The new rating (0-5)
        :param category: The new category
        :param tags: The new tags - this overrides the existing tags
        :param path: The new path - this does NOT move the file but can be useful for updating the path if it has
         changed
        :return:
        """
        self.__api.put(f'assets/{id_}', json={
            'description': description,
            'rating': rating,
            'category': category,
            'tags': tags,
            'path': str(path)
        })

    def wait_for_asset(self, path: Path, timeout: int = 60) -> AssetModel:
        """
        Waits for the current indexing job to finish
        """
        start = time.time()
        while time.time() < start + timeout:
            try:
                return self.get_asset_by_path(path)
            except Exception as e:
                print(f"Waiting for asset to index: {path}, not yet available because: {e}")
            time.sleep(1)

        raise Exception(f"Timed out waiting for asset to index: {path}")

    def delete_all_assets(self) -> None:
        """
        WARNING deletes all assets in the database
        :return:
        """
        self.__api.delete(f'assets')

    def get_faces(self, id_: uuid.UUID) -> List[dict]:
        faces = self.__api.get(f'assets/{id_}/faces')

        return faces.json()
