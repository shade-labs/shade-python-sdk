from uuid import UUID

import requests

from .abc_resource import ABCResource


class Billing(ABCResource):
    def get_workspace_usage(self, workspace: UUID | dict):
        """
        Return the usage of the given workspace
        :param workspace: The workspace or the id of the workspace
        :return: The usage
        """
        if isinstance(workspace, dict):
            workspace = workspace['id']

        resp = requests.get(
            self.auth.remote_url + f'/workspaces/{workspace}/usage',
            headers={'Authorization': self.auth.api_key},
        )
        resp.raise_for_status()
        return resp.json()
