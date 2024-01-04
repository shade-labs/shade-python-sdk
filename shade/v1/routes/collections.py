# TODO collections an asset belongs in, collection info (/collections/collection_id), list all
#  collections, delete collection, add assets to collection, delete assets from collection
from shade.v1.api import API
from shade.v1.types import MountInfo


class Collections:
    def __init__(self, api: API, mount_info: MountInfo):
        self.__api = api
        self.__mount_info = mount_info

    def get_collections(self):
        return self.__api.get('collections').json()
