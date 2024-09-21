from .abc_resource import ABCResource
from pydantic import BaseModel
from uuid import UUID
from typing import List


class WorkspaceModel(BaseModel):
    id: UUID
    name: str
    description: str
    domain: str



class Workspace(ABCResource):
    def get_workspaces(self) -> List[WorkspaceModel]:
        pass

    def get_workspace_by_id(self, id_: UUID) -> WorkspaceModel:
        pass

    def get_workspace_by_name(self, name: str) -> WorkspaceModel:
        """
        Return the first matching workspace to the given name
        :param name: The name of the workspace
        :return: The workspace
        """
        workspaces = self.get_workspaces()

        for workspace in workspaces:
            if workspace.name == name:
                return workspace

        raise ValueError(f'No workspace with name {name}')
