# TODO pause, unpause indexing, resync, indexing status / queue size, reset
from shade.v1.api import API
from shade.v1.types import MountInfo


class Indexing:
    def __init__(self, api: API, mount_info: MountInfo):
        self.__api = api
        self.__mount_info = mount_info

    def resync(self):
        self.__api.post('indexing/sync')
