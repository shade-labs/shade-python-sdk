from shade import Shade
from shade.query_builder import FilterBuilder, QueryBuilder

shade = Shade(api_key='key')

workspace = shade.workspace.get_workspace_by_name('Your Personal Workspace')

drive = shade.drive.get_drive_by_name('Drive Name')

shade.asset.search(drive, QueryBuilder().set_query('people by the ocean')
.add_filter(
    FilterBuilder().date_created.before.set_options({
        'date': '2021-01-01'
    }).finish()
).add_filter(
    FilterBuilder().file_type.is_.set_options([
        'VIDEO'
    ]).finish()
)
.page(2)
.limit(50)
.threshold(0).finish())
