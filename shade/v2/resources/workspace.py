from uuid import UUID

import requests

from .abc_resource import ABCResource


class Workspace(ABCResource):
    def get_workspaces(self) -> dict:
        resp = requests.get(
            self.auth.remote_url + '/workspaces',
            headers={'Authorization': self.auth.api_key},
        )
        resp.raise_for_status()
        return resp.json()

    def get_workspace_by_id(self, id_: UUID) -> dict:
        """
        Return the workspace with the given id
        :param id_: The id of the workspace
        :return: The workspace
        """
        resp = requests.get(
            self.auth.remote_url + f'/workspaces/{id_}',
            headers={'Authorization': self.auth.api_key},
        )
        resp.raise_for_status()
        return resp.json()

    def get_workspace_by_name(self, name: str) -> dict:
        """
        Return the first matching workspace to the given name
        :param name: The name of the workspace
        :return: The workspace
        """
        workspaces = self.get_workspaces()

        for workspace in workspaces:
            if workspace['name'] == name:
                return workspace

        raise ValueError(f'No workspace with name {name}')

    def create_workspace(self):
        raise NotImplementedError
