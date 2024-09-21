from uuid import UUID
from .abc_resource import ABCResource
import requests

class Drive(ABCResource):
    def get_drives(self, workspace: dict | UUID):
        if isinstance(workspace, dict):
            workspace = workspace['id']

        resp = requests.get(self.auth.remote_url + f'/workspaces/{workspace}/drives', headers={'Authorization': self.auth.api_key})
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
