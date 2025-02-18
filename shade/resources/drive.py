from typing import Optional
from uuid import UUID

import requests

from ..enums import DriveIconType, DriveType, MetadataAttribute
from .abc_resource import ABCResource


class Drive(ABCResource):
    def get_drives(self, workspace: dict | UUID):
        if isinstance(workspace, dict):
            workspace = workspace['id']

        resp = requests.get(
            self.auth.remote_url + f'/workspaces/{workspace}/drives',
            headers={'Authorization': self.auth.api_key},
        )
        resp.raise_for_status()
        return resp.json()

    def get_drive_by_id(self, workspace: dict | UUID, id_: UUID):
        if isinstance(workspace, dict):
            workspace = workspace['id']

        drives = self.get_drives(workspace)
        for drive in drives:
            if drive['id'] == id_:
                return drive

        raise ValueError(f'No drive with id {id_}')

    def get_drive_by_name(self, workspace: dict | UUID, name: str):
        if isinstance(workspace, dict):
            workspace = workspace['id']

        drives = self.get_drives(workspace)
        for drive in drives:
            if drive['name'] == name:
                return drive

        raise ValueError(f'No drive with name {name}')

    def create_drive(
        self,
        workspace: dict | UUID,
        name: str,
        description: str,
        icon: Optional[str] = '',
        icon_type: DriveIconType = DriveIconType.COLOR,
        type: DriveType = DriveType.MAGIC,
    ):
        if isinstance(workspace, dict):
            workspace = workspace['id']

        resp = requests.post(
            self.auth.remote_url + f'/workspaces/{workspace}/drives',
            headers={'Authorization': self.auth.api_key},
            json={
                'name': name,
                'description': description,
                'icon': icon,
                'icon_type': icon_type.value,
                'type': type.value,
            },
        )
        resp.raise_for_status()
        return resp.json()

    def get_custom_metadata(self, drive: dict | UUID):
        if isinstance(drive, dict):
            drive = drive['id']

        resp = requests.get(
            self.auth.remote_url + f'/workspaces/drives/{drive}/custom-metadata',
            headers={'Authorization': self.auth.api_key},
        )
        resp.raise_for_status()
        return resp.json()

    def add_drive_metadata(self, drive: dict | UUID, metadata: MetadataAttribute):
        """Add metadata attributes to a drive.

        Args:
            drive: Drive ID or drive dict object
            metadata: Dictionary containing the metadata attributes
        """
        if isinstance(drive, dict):
            drive = drive['id']

        resp = requests.post(
            self.auth.remote_url + f'/workspaces/drives/{drive}/metadata',
            headers={'Authorization': self.auth.api_key},
            json=metadata.model_dump(mode='json'),
        )
        resp.raise_for_status()
        return resp.json()
