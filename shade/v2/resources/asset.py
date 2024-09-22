from .abc_resource import ABCResource
from ..query_builder import ComposableQuery
from uuid import UUID


class Asset(ABCResource):
    def search(self, drive: UUID | dict, query: ComposableQuery):
        if isinstance(drive, dict):
            drive = drive.get('id')


