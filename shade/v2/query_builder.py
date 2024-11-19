from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class FilterQuery(BaseModel):
    id: str
    clause: str
    options: dict


class FilterBuilder:
    id: str
    clause: str
    options: dict

    @property
    def audio_loop(self) -> "FilterBuilder":
        self.id = "audio_loop"
        return self

    @property
    def bpm(self) -> "FilterBuilder":
        self.id = "bpm"
        return self

    @property
    def collection(self) -> "FilterBuilder":
        self.id = "collection"
        return self

    @property
    def color(self) -> "FilterBuilder":
        self.id = "color"
        return self

    @property
    def date_created(self) -> "FilterBuilder":
        self.id = "date_created"
        return self

    @property
    def date_modified(self) -> "FilterBuilder":
        self.id = "date_modified"
        return self

    @property
    def date_indexed(self) -> "FilterBuilder":
        self.id = "date_indexed"
        return self

    @property
    def file_category(self) -> "FilterBuilder":
        self.id = "file_category"
        return self

    @property
    def file_extension(self) -> "FilterBuilder":
        self.id = "file_extension"
        return self

    @property
    def file_type(self) -> "FilterBuilder":
        self.id = "file_type"
        return self

    @property
    def path(self) -> "FilterBuilder":
        self.id = "path"
        return self

    @property
    def individual(self) -> "FilterBuilder":
        self.id = "individual"
        return self

    @property
    def key(self) -> "FilterBuilder":
        self.id = "key"
        return self

    @property
    def photo_feature(self) -> "FilterBuilder":
        self.id = "photo_feature"
        return self

    @property
    def rating(self) -> "FilterBuilder":
        self.id = "rating"
        return self

    @property
    def resolution(self) -> "FilterBuilder":
        self.id = "resolution"
        return self

    @property
    def tag(self) -> "FilterBuilder":
        self.id = "tag"
        return self

    @property
    def ai_tag(self) -> "FilterBuilder":
        self.id = "ai_tag"
        return self

    @property
    def job_state(self) -> "FilterBuilder":
        self.id = "job_state"
        return self

    @property
    def name(self) -> "FilterBuilder":
        self.id = "name"
        return self

    @property
    def is_(self) -> "FilterBuilder":
        self.clause = "is"
        return self

    @property
    def is_any_of(self) -> "FilterBuilder":
        self.clause = "is any of"
        return self

    @property
    def is_not(self) -> "FilterBuilder":
        self.clause = "is not"
        return self

    @property
    def has(self) -> "FilterBuilder":
        self.clause = "has"
        return self

    @property
    def has_not(self) -> "FilterBuilder":
        self.clause = "has not"
        return self

    @property
    def before(self) -> "FilterBuilder":
        self.clause = "before"
        return self

    @property
    def after(self) -> "FilterBuilder":
        self.clause = "after"
        return self

    @property
    def between(self) -> "FilterBuilder":
        self.clause = "between"
        return self

    @property
    def in_(self) -> "FilterBuilder":
        self.clause = "is directly in"
        return self

    @property
    def under(self) -> "FilterBuilder":
        self.clause = "is under"
        return self

    @property
    def not_in(self) -> "FilterBuilder":
        self.clause = "is not in"
        return self

    @property
    def less(self) -> "FilterBuilder":
        self.clause = "less"
        return self

    @property
    def less_any_of(self) -> "FilterBuilder":
        self.clause = "less than any of"
        return self

    @property
    def less_equal(self) -> "FilterBuilder":
        self.clause = "less/equal"
        return self

    @property
    def less_equal_any_of(self) -> "FilterBuilder":
        self.clause = "less/equal than any of"
        return self

    @property
    def greater(self) -> "FilterBuilder":
        self.clause = "greater"
        return self

    @property
    def greater_any_of(self) -> "FilterBuilder":
        self.clause = "greater any of"
        return self

    @property
    def greater_equal(self) -> "FilterBuilder":
        self.clause = "greater/equal"
        return self

    @property
    def greater_equal_any_of(self) -> "FilterBuilder":
        self.clause = "greater/equal any of"
        return self

    @property
    def not_started(self) -> "FilterBuilder":
        self.clause = "hasn't started"
        return self

    @property
    def in_progress(self) -> "FilterBuilder":
        self.clause = "in progress of"
        return self

    @property
    def completed(self) -> "FilterBuilder":
        self.clause = "completed"
        return self

    @property
    def failed(self) -> "FilterBuilder":
        self.clause = "failed"
        return self

    @property
    def includes(self) -> "FilterBuilder":
        self.clause = "includes"
        return self

    @property
    def not_includes(self) -> "FilterBuilder":
        self.clause = "does not include"
        return self

    @property
    def starts_with(self) -> "FilterBuilder":
        self.clause = "starts with"
        return self

    @property
    def ends_with(self) -> "FilterBuilder":
        self.clause = "end with"
        return self

    def set_options(self, options: dict | list) -> "FilterBuilder":
        self.options = options
        return self

    def finish(self) -> FilterQuery:
        return FilterQuery(id=self.id, clause=self.clause, options=self.options)


class ComposableQuery(BaseModel):
    query: Optional[str] = None
    similar_asset_id: Optional[UUID] = None
    filters: list[FilterQuery] = []
    limit: Optional[int] = None
    page: Optional[int] = None
    threshold: Optional[float] = None


class QueryBuilder:
    query: ComposableQuery = ComposableQuery()

    def set_query(self, query: str) -> "QueryBuilder":
        self.query.query = query
        return self

    def set_similar_asset(self, asset: UUID | dict) -> "QueryBuilder":
        if isinstance(asset, dict):
            self.query.similar_asset_id = asset.get("id")

        self.query.similar_asset_id = asset
        return self

    def add_filter(self, filter_: FilterQuery) -> "QueryBuilder":
        self.query.filters.append(filter_)
        return self

    def limit(self, limit: int) -> "QueryBuilder":
        self.query.limit = limit
        return self

    def page(self, page: int) -> "QueryBuilder":
        self.query.page = page
        return self

    def threshold(self, threshold: int) -> "QueryBuilder":
        self.query.threshold = threshold
        return self

    def finish(self) -> ComposableQuery:
        return self.query
