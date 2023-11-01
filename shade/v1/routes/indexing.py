# TODO pause, unpause indexing, resync, indexing status / queue size,
#  reset
import time
import uuid
from pathlib import Path

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

    def reset_indexing(self):
        """
        Reset the indexing process.
        This will remove previews as well.

        Warning this is a destructive action
        :return:
        """
        self.__api.post('indexing/reset')

    def queue_single_file(self, path: Path) -> uuid.UUID:
        response = self.__api.post('indexing/file', json={
            'path': str(self.__mount_info.translate_filepath_to_server(path))
        })

        return uuid.UUID(response.json())

    def wait_for_indexing(self):
        """
        Waits for the current indexing job to finish
        """
        while True:
            status = self.status()
            if status['state'] == 'IDLE':
                break
            print(f"Waiting for indexing to finish, {status['state']}. "
                  f"Progress: {status['progress']}/{status['total']}")
            time.sleep(1)


