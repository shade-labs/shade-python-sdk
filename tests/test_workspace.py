import pytest

from shade import Shade
from tests.helpers import get_random_string

# ToDo - do something better w this once we add it to GH actions
API_KEY = 'sk_965a8a31cbf49c8ecc842082d40d5fa8cc529aa78a217788536cbeff5cf56ab3'
REMOTE_URL = 'http://127.0.0.1:9082'


# shade = Shade(remote_url=REMOTE_URL, api_key=API_KEY)


@pytest.fixture
def shade():
    return Shade(remote_url=REMOTE_URL, api_key=API_KEY)


def test_create_and_get_workspace(
    shade: Shade,
):
    """Test a crud route for a member to create a drive in a workspace"""

    workspace_data = {
        'name': "Clarkson's Farm",
        'description': 'Clarkson and his team are back on the farm',
        'thumbnail': 'manymanybytez',
        'domain': get_random_string(5),
    }

    created_workspace = shade.workspace.create_workspace(**workspace_data)

    assert created_workspace
    assert created_workspace.get('name') == workspace_data.get('name')
    assert created_workspace.get('description') == workspace_data.get('description')
    assert created_workspace.get('thumbnail') == workspace_data.get('thumbnail')

    get_2 = shade.workspace.get_workspace_by_domain(created_workspace.get('domain'))

    get_1 = shade.workspace.get_workspace_by_id(created_workspace.get('id'))
    assert get_1.get('name') == get_2.get('name') == created_workspace.get('name')
