from pathlib import Path

from shade import Shade
from shade.query_builder import QueryBuilder
from shade.resources.share import DriveRole


def test_get_folders(shade: Shade, test_drive):
    drive = test_drive

    folders = shade.asset.listdir_folders(
        drive=drive.get('id'),
        path=Path('/'),
        page=0,
        limit=100,  # Returns the path of the folder
    )

    folders_in_base = [folder_bits.split('/')[-1] for folder_bits in folders]

    assert set(folders_in_base) == {'folder_1', 'folder_2', '.trash'}

    assert len(folders) == 3


def test_get_files(shade: Shade, test_drive):
    drive = test_drive

    assets = shade.asset.listdir_files(
        drive=drive, path=Path('/folder_1/'), page=0, limit=100
    )

    assert len(assets) == 2


def test_share_file(shade: Shade, test_drive):
    drive = test_drive
    shared_asset_path = f'/{test_drive.get("id")}/folder_1/test_1.jpg'

    shared = shade.share.share_asset(
        drive=drive,
        asset_path=Path(shared_asset_path),
        email='emerson@shade.inc',
        role=DriveRole.EDITOR,
        message='Hello you are invited',
    )

    assert shared is True

    # todo verify this is actually shared


def test_share_folder(shade: Shade, test_drive):
    drive = test_drive
    shared_folder_path = f'/{test_drive.get("id")}/folder_2'

    shared = shade.share.share_asset(
        drive=drive,
        asset_path=Path(shared_folder_path),
        email='emerson@shade.inc',
        role=DriveRole.EDITOR,
        message='Hello you are invited',
    )

    assert shared is True

    # todo verify this is actually shared


def test_delete_asset(shade: Shade, test_drive):
    drive = test_drive
    shared_asset_path = f'/{test_drive.get("id")}/folder_1/test_1.jpg'

    assets = shade.asset.listdir_files(
        drive=drive, path=Path('/folder_1/'), page=0, limit=100
    )
    assert len(assets) == 2

    # this fails bc of FS stuff.
    deleted = shade.asset.delete_asset(drive=drive, path=Path(shared_asset_path))
    assert deleted is True

    assets = shade.asset.listdir_files(
        drive=drive, path=Path('/folder_1/'), page=0, limit=100
    )

    assert len(assets) == 1


def test_search_in_folder(shade: Shade, test_drive):
    drive_id = test_drive.get('id')

    files = shade.asset.listdir_files(
        drive=test_drive,
        query=QueryBuilder()
        .set_query('image')
        .set_path(f'/{drive_id}/folder_1/')
        .limit(50)
        .threshold(0)
        .finish(),
    )

    # ToDo: once we have the uploader, test for an actual query like "City"
    assert len(files) == 0


def test_search_similar(shade: Shade, test_drive):
    assets = shade.asset.listdir_files(
        drive=test_drive, path=Path('/folder_1/'), page=0, limit=100
    )
    files = shade.asset.listdir_files(
        drive=test_drive,
        query=QueryBuilder()
        .set_similar_asset(assets[0])
        .set_path('/38d862c3-7699-4ff0-b0fc-9be89c2f85af/')
        .limit(50)
        .threshold(0)
        .finish(),
    )

    assert len(files) == 0
    # ToDo: once we have the uploader, test for actual similar files


def test_update_asset(shade: Shade, test_drive):
    assets = shade.asset.listdir_files(
        drive=test_drive, path=Path('/folder_1/'), page=0, limit=100
    )
    asset = assets[0]

    update = shade.asset.update_asset(
        drive=test_drive,
        asset=asset,
        rating=4,
        category='New Category',
    )
    assert update.get('rating') == 4.0
    assert update.get('rating') != asset.get('rating')
