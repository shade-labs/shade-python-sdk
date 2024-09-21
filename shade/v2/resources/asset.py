from .abc_resource import ABCResource
from ..query_builder import ComposableQuery


class Asset(ABCResource):
    def search(self, query: ComposableQuery):
        pass
