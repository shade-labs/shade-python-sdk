from pathlib import Path

from shade.v2 import Shade
from shade.v2.resources.share import DriveRole

REMOTE_URL = 'http://127.0.0.1:9082'

# this is fine, it's a test key... should probably make an env thingy
API_KEY = 'sk_eeb5f87e66bc3120f9b324e1204a050e41d6fe957966fe3cc51064c14edf1d5e'

if __name__ == '__main__':
    shade = Shade(remote_url=REMOTE_URL, api_key=API_KEY)

    # workspaces = shade.workspace.get_workspaces()
    workspace = shade.workspace.get_workspace_by_domain('shade-workspace')

    # print('workspace', workspace)

    drives = shade.drive.get_drives(workspace)

    drive = drives[0]

    assets = shade.asset.listdir_files(drive=drive, path=Path('/'), page=0, limit=100)
    # print('assets', assets)

    folders = shade.asset.listdir_folders(
        drive=drive.get('id'), path=Path('/'), page=0, limit=100
    )
    # print(folders)

    if shade.share.share_asset(
        drive=drive,
        asset_path=Path(assets[0].get('path')),
        email='emerson@shade.inc',
        role=DriveRole.EDITOR,
        url='https://shade.inc',
        message='Hello',
    ):
        print('Shared file with user')
