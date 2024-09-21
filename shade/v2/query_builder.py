from pydantic import BaseModel
from typing import Optional


class ComposableQuery(BaseModel):
    query: Optional[str] = None


class QueryBuilder:
    query: ComposableQuery = ComposableQuery()

    def set_query(self, query: str) -> 'QueryBuilder':
        self.query.query = query
        return self

    def finish(self) -> ComposableQuery:
        return self.query
