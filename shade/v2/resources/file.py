from shade.v2.resources.abc_resource import ABCResource
from uuid import UUID
from pathlib import Path
import requests

class File(ABCResource):
    def mkdir(self, drive: UUID | dict, path: Path):
        if isinstance(drive, dict):
            drive = drive.get('id')

        resp = requests.post(self.auth.remote_url + '/files/directory',
                             headers={'Authorization': self.auth.api_key},
                             json={
                                 'drive_id': drive,
                                 'path': f'/{drive}{path}',
                             })

        resp.raise_for_status()
