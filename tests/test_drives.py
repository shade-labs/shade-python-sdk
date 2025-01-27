from shade import Shade


def test_create_and_get_drives(shade: Shade, test_workspace):
    drive_data = {
        'workspace': test_workspace,
        'name': 'This is a cool drive',
        'description': 'Season 3',
    }
    drive_res = shade.drive.create_drive(**drive_data)

    print(drive_res)

    dr_1 = shade.drive.get_drive_by_id(test_workspace, drive_res.get('id'))

    assert dr_1.get('name') == drive_res.get('name') == drive_data.get('name')

    dr_2 = shade.drive.get_drive_by_name(test_workspace, drive_res.get('name'))

    assert dr_2.get('name') == drive_res.get('name') == drive_data.get('name')

    workspace_drives = shade.drive.get_drives(test_workspace)
    print(workspace_drives)

    assert len(workspace_drives) == 1
