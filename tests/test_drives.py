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


#     """Test a crud route for a member to create a drive in a workspace"""
#
#     workspace_data = {
#         'name': "Clarkson's Farm",
#         'description': 'Clarkson and his team are back on the farm',
#         'thumbnail': 'manymanybytez',
#         'domain': get_random_string(5),
#     }
#
#     create_workspace_res = shade.workspace.create_workspace(**workspace_data)
#
#     assert create_workspace_res
#     assert create_workspace_res.get('name') == workspace_data.get('name')
#     assert create_workspace_res.get('description') == workspace_data.get('description')
#     assert create_workspace_res.get('thumbnail') == workspace_data.get('thumbnail')
#
#     get_2 = shade.workspace.get_workspace_by_domain(create_workspace_res.get('domain'))
#
#     get_1 = shade.workspace.get_workspace_by_id(create_workspace_res.get('id'))
#     get_3 = shade.workspace.get_workspace_by_name(get_2.get('name'))
#     assert (
#         get_1.get('name')
#         == get_2.get('name')
#         == get_3.get('name')
#         == create_workspace_res.get('name')
#     )
#
#
# def test_create_and_delete_workspace(
#     shade: Shade,
# ):
#     """Test a crud route for a member to create a drive in a workspace"""
#
#     workspace_data = {
#         'name': "Clarkson's Farm",
#         'description': 'Clarkson and his team are back on the farm',
#         'thumbnail': 'manymanybytez',
#         'domain': get_random_string(5),
#     }
#
#     create_workspace_res = shade.workspace.create_workspace(**workspace_data)
#     create_workspace_id = create_workspace_res.get('id')
#
#     created_workspace = shade.workspace.get_workspace_by_id(create_workspace_id)
#
#     assert created_workspace
#
#     delete_workspace_response = shade.workspace.delete_workspace(create_workspace_id)
#
#     assert delete_workspace_response is True
#
#     with pytest.raises(Exception, match='404'):
#         # make sure the workspace doesn't exist anymore
#         shade.workspace.get_workspace_by_id(create_workspace_id)
