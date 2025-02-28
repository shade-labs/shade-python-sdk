import os
import sys
import threading
from pathlib import Path
from typing import Any, Optional
from uuid import UUID
import subprocess

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

    def update_asset_metadata(
        self,
        drive: UUID | dict,
        asset: UUID | dict,
        metadata_attribute_id: str = None,
        metadata_attribute_value: Optional[Any] = None,
    ) -> bool:
        if isinstance(drive, dict):
            drive = drive.get('id')
        if isinstance(asset, dict):
            asset = asset.get('id')

        body = {'drive_id': drive, 'metadata_attribute_value': metadata_attribute_value}

        resp = requests.put(
            self.auth.remote_url
            + f'/assets/{asset}/metadata/{metadata_attribute_id}/value',
            headers={'Authorization': self.auth.api_key},
            json=body,
        )

        resp.raise_for_status()

        return resp.json()

    def get_signed_download_url(
        self,
        drive: UUID | dict,
        path: Path,
    ) -> str:
        path = str(path)

        if isinstance(drive, dict):
            drive = drive.get('id')

        if not path.startswith(f'/{drive}'):
            raise ValueError('Asset path must start with /{drive_id}')

        resp = requests.get(
            self.auth.remote_url + '/files/download',
            headers={'Authorization': self.auth.api_key},
            params={'drive_id': drive, 'path': path, 'download': True},
        )

        resp.raise_for_status()

        return resp.json()

    @staticmethod
    def __print_stream(stream, stderr: bool = False):
        for line in iter(stream.readline, b''):
            print(line.decode().strip(), file=sys.stderr if stderr else sys.stdout)

    def upload_using_external_uploader(
        self,
        uploader_path: Path,
        drive: UUID | dict,
        directory: Path,
        destination: str = '/',
    ):
        """
        Using the uploader binary, upload a directory to the specified drive
        """
        if isinstance(drive, dict):
            drive = drive.get('id')

        popen = subprocess.Popen([
            str(uploader_path),
            '--mode',
            'directory',
            '--directory',
            str(directory),
            '--drive',
            str(drive),
            '--key',
            self.auth.api_key,
            '--destination',
            str(destination),
        ], env={
            **os.environ,
            'SHADE_API_URL': self.auth.remote_url,
            'FS_API_URL': self.auth.fs_url,
            'FS_WS_URL': self.auth.fs_url.replace('https://', 'wss://') if self.auth.fs_url.startswith('https://') else self.auth.fs_url.replace('http://', 'ws://'),
        },
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

        stdout = threading.Thread(target=self.__print_stream, args=(popen.stdout,))
        stderr = threading.Thread(target=self.__print_stream, args=(popen.stderr, True))

        # Start streaming
        stdout.start()
        stderr.start()

        # Wait for the process
        popen.wait()

        # Close the streams
        popen.stdout.close()
        popen.stderr.close()

        # Join the threads and we're done
        stdout.join()
        stderr.join()

