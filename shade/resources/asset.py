from pathlib import Path
from typing import Optional
from uuid import UUID

import requests

from ..query_builder import ComposableQuery
from .abc_resource import ABCResource


class Asset(ABCResource):
    def search(self, drive: UUID | dict, query: ComposableQuery) -> list[dict]:
        if isinstance(drive, dict):
            drive = drive.get('id')

        data = query.model_dump()
        data['drive_id'] = drive

        print('Data', data)

        resp = requests.post(
            self.auth.remote_url + '/search',
            headers={'Authorization': self.auth.api_key},
            json=data,
        )
        resp.raise_for_status()

        return resp.json()

    def listdir_files(
        self,
        drive: UUID | dict,
        path: Path = Path('/'),
        page: int = 0,
        limit: int = 100,
        query: ComposableQuery = None,
    ) -> list[dict]:
        if isinstance(drive, dict):
            drive = drive.get('id')

        print(query.model_dump() if query else {})

        resp = requests.post(
            self.auth.remote_url + '/search/files',
            headers={'Authorization': self.auth.api_key},
            json={
                'drive_id': drive,
                'path': f'/{drive}{path}',
                'page': page,
                'limit': limit,
            }
            | (query.model_dump() if query else {}),
        )

        resp.raise_for_status()

        return resp.json()

    def listdir_folders(
        self,
        drive: UUID | dict,
        path: Path = Path('/'),
        page: int = 0,
        limit: int = 100,
        query: str = None,
    ) -> list[str]:
        if isinstance(drive, dict):
            drive = drive.get('id')

        resp = requests.get(
            self.auth.remote_url + '/search/folders',
            headers={'Authorization': self.auth.api_key},
            params={
                'drive_id': drive,
                'path': f'/{drive}{path}',
                'page': page,
                'limit': limit,
                'query': query,
            },
        )

        resp.raise_for_status()

        return resp.json()

    def delete_asset(self, drive: UUID | dict, path: Path) -> bool:
        if isinstance(drive, dict):
            drive = drive.get('id')

        resp = requests.post(
            self.auth.remote_url + '/files/trash',
            headers={'Authorization': self.auth.api_key},
            json={
                'path': str(path),
                'drive_id': drive,
            },
        )

        resp.raise_for_status()

        return resp.status_code == 200

    def update_asset(
        self,
        drive: UUID | dict,
        asset: UUID | dict,
        rating: Optional[int],
        category: Optional[str],
    ) -> bool:
        if isinstance(drive, dict):
            drive = drive.get('id')
        if isinstance(asset, dict):
            asset = asset.get('id')

        body = {
            'drive_id': drive,
        }

        if category:
            body['category'] = category

        if rating:
            body['rating'] = rating

        resp = requests.put(
            self.auth.remote_url + f'/assets/{asset}',
            headers={'Authorization': self.auth.api_key},
            json=body,
        )

        resp.raise_for_status()

        return resp.json()

    def get_signed_download_url(
        self,
        drive: UUID | dict,
        asset: UUID | dict,
    ) -> str:
        # if isinstance(asset, dict):
        #     asset = asset.get('id')
        if isinstance(drive, dict):
            drive = drive.get('id')

        path = asset.get('path')

        if not path.startswith(f'/{drive}'):
            raise ValueError('Asset path must start with /{drive_id}')

        resp = requests.get(
            self.auth.remote_url + '/files/download',
            headers={'Authorization': self.auth.api_key},
            params={'drive_id': drive, 'path': asset.get('path'), 'download': True},
        )

        resp.raise_for_status()

        return resp.json()
