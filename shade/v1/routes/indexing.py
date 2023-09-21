# TODO pause, unpause indexing, resync, indexing status / queue size, reset
from shade.v1.api import API
from shade.v1.types import MountInfo


class Indexing:
    def __init__(self, api: API, mount_info: MountInfo):
        self.__api = api
        self.__mount_info = mount_info

    def resync(self):
        self.__api.post('indexing/sync')

    def pause(self):
        self.__api.post('indexing/pause', json={
            'pause': True
        })

    def resume(self):
        self.__api.post('indexing/pause', json={
            'pause': False
        })

    def status(self) -> dict:
        """
        Get the information about the indexing process

        TODO make this a pydantic model
        :return: The indexing status
        """
        return self.__api.get('indexing/status').json()

    def get_queue(self) -> list:
        """
        Get the queue of files to be indexed

        TODO make this a pydantic model
        :return: The queue
        """
        return self.__api.get('indexing/queue').json()
