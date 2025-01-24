from pathlib import Path

from shade import Shade
from shade.query_builder import QueryBuilder
from shade.resources.share import DriveRole

REMOTE_URL = 'http://127.0.0.1:9082'

# this is fine, it's a test key... should probably make an env thingy
API_KEY = 'sk_965a8a31cbf49c8ecc842082d40d5fa8cc529aa78a217788536cbeff5cf56ab3'

if __name__ == '__main__':
    shade = Shade(remote_url=REMOTE_URL, api_key=API_KEY)

    # workspaces = shade.workspace.get_workspaces()
    workspace = shade.workspace.get_workspace_by_domain('sebs-playground')

    # print('workspace', workspace)

    drives = shade.drive.get_drives(workspace)

    drive = drives[0]

    assets = shade.asset.listdir_files(
        drive=drive, path=Path('/'), page=0, limit=100
    )  # Note: returns the full assset
    print('assets', assets)

    folders = shade.asset.listdir_folders(
        drive=drive.get('id'),
        path=Path('/'),
        page=0,
        limit=100,  # Returns the path of the folder
    )
    print(folders)

    def share_file():
        if shade.share.share_asset(
            drive=drive,
            asset_path=Path(assets[0].get('path')),
            email='emerson@shade.inc',
            role=DriveRole.EDITOR,
            message='Hello you are invited',
        ):
            print('Shared file with user')

    share_file()

    def share_folder():
        if shade.share.share_asset(
            drive=drive,
            asset_path=Path(folders[0]),
            email='emerson@shade.inc',
            role=DriveRole.EDITOR,
            message='Hello',
        ):
            print('Shared folder with user')

    share_folder()

    def delete_asset():
        resp = shade.asset.delete_asset(drive=drive, path=Path(assets[0].get('path')))
        if resp:
            print('Deleted asset')

    # delete_asset() Todo only uncomment if there is an asset to delete on the top level of the drive

    def search_in_folder():
        files = shade.asset.listdir_files(
            drive=drive,
            query=QueryBuilder()
            .set_query('city')
            .set_path('/38d862c3-7699-4ff0-b0fc-9be89c2f85af/shade_tests/places/nyc')
            .limit(50)
            .threshold(0)
            .finish(),
        )

        print(len(files))

    # search_in_folder()

    def search_similar():
        files = shade.asset.listdir_files(
            drive=drive,
            query=QueryBuilder()
            .set_similar_asset(assets[0])
            .set_path('/38d862c3-7699-4ff0-b0fc-9be89c2f85af/')
            .limit(50)
            .threshold(0)
            .finish(),
        )
        print(files)

    search_similar()

    def update_asset():
        update = shade.asset.update_asset(
            drive=drive,
            asset=assets[0],
            description='This is a new description',
            rating=5,
            category='New Category',
        )

        print(update)

    update_asset()
