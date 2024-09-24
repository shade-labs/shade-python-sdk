from .abc_resource import ABCResource
from ..query_builder import ComposableQuery
from uuid import UUID
import requests
from typing import List


class Asset(ABCResource):
    def search(self, drive: UUID | dict, query: ComposableQuery) -> List[dict]:
        if isinstance(drive, dict):
            drive = drive.get('id')

        data = query.model_dump()
        data['drive_id'] = drive

        resp = requests.post(self.auth.remote_url + '/search',
                             headers={'Authorization': self.auth.api_key},
                             json=data)
        resp.raise_for_status()

        return resp.json()
