from enum import Enum
from pathlib import Path
from uuid import UUID

import requests

from .abc_resource import ABCResource


class DriveRole(int, Enum):
    ADMIN = 50
    FULL_ACCESS = 40
    EDITOR = 30
    COMMENTER = 20
    DOWNLOADER = 17
    VIEWER = 15
    METADATA_VIEWER = 10
    NONE = 0


class Share(ABCResource):
    def share_asset(
        self,
        drive: UUID | dict,
        asset_path: Path,
        email: str,
        role: DriveRole,
        url,
        message,
    ) -> dict:
        if isinstance(drive, dict):
            drive = drive.get('id')

        resp = requests.post(
            self.auth.remote_url + f'/workspaces/drives/{drive}/share-file',
            headers={'Authorization': self.auth.api_key},
            json={
                'path': str(asset_path),
                'invites': [
                    {
                        'email': email,
                        'role': role.value,
                    }
                ],
                'url': url,
                'message': message,
            },
        )
        resp.raise_for_status()
        return resp.json()
