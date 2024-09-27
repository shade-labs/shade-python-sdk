from pathlib import Path
from typing import List
from uuid import UUID

import requests

from .abc_resource import ABCResource
from ..query_builder import ComposableQuery


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

    def listdir_files(self, drive: UUID | dict, path: Path = Path('/'), page: int = 0, limit: int = 100,
                      query: ComposableQuery = None) -> List[dict]:
        if isinstance(drive, dict):
            drive = drive.get('id')

        resp = requests.post(self.auth.remote_url + '/search/files',
                             headers={'Authorization': self.auth.api_key},
                             json={
                                      'drive_id': drive,
                                      'path': f'/{drive}{path}',
                                      'page': page,
                                      'limit': limit,
                                  } | (query.model_dump() if query else {}))

        resp.raise_for_status()

        return resp.json()

    def listdir_folders(self, drive: UUID | dict, path: Path = Path('/'), page: int = 0, limit: int = 100,
                        query: str = None) -> List[str]:
        if isinstance(drive, dict):
            drive = drive.get('id')

        resp = requests.get(self.auth.remote_url + '/search/folders',
                             headers={'Authorization': self.auth.api_key},
                             params={
                                 'drive_id': drive,
                                 'path': f'/{drive}{path}',
                                 'page': page,
                                 'limit': limit,
                                 'query': query
                             })

        resp.raise_for_status()

        return resp.json()
