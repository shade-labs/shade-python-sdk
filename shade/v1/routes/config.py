# get/set config. Add/remove models
# TODO pause, unpause indexing, resync, indexing status / queue size, reset
from shade.v1.api import API
from shade.v1.types import MountInfo


class Config:
    def __init__(self, api: API, mount_info: MountInfo):
        self.__api = api
        self.__mount_info = mount_info

    def get_config(self) -> dict:
        # TODO make this a pydantic model
        return self.__api.get('config').json()
