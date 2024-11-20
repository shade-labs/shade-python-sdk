from pathlib import Path
from uuid import UUID

import requests

from shade.v2.resources.abc_resource import ABCResource


class File(ABCResource):
    def mkdir(self, drive: UUID | dict, path: Path):
        if isinstance(drive, dict):
            drive = drive.get('id')

        resp = requests.post(
            self.auth.remote_url + '/files/directory',
            headers={'Authorization': self.auth.api_key},
            json={
                'drive_id': drive,
                'path': f'/{drive}{path}',
            },
        )

        resp.raise_for_status()

    def mv(self, drive: UUID | dict, source: Path, destination: Path):
        """
        Move a folder or file to one location to another. The destination folder must exist and the destination file
        must not already exist

        :param drive: drive uuid
        :param source: the file or folder to move from
        :param destination: to location to move it to
        :return: None
        """
        if isinstance(drive, dict):
            drive = drive.get('id')

        resp = requests.post(
            self.auth.remote_url + '/files/move',
            headers={'Authorization': self.auth.api_key},
            json={
                'drive_id': drive,
                'source': f'/{drive}{source}',
                'destination': f'{drive}{destination}',
            },
        )

        resp.raise_for_status()
