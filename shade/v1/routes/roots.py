import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

from shade.v1.api import API
from shade.v1.types import PathConverter
from typing import List


class RootModel(PathConverter):
    id: uuid.UUID
    path: Path
    created: datetime
    updated: datetime
    files_found: int = 0
    size_bytes: int = 0

    is_directory: bool

    ctime: Optional[datetime] = None
    mtime: Optional[datetime] = None


class Roots:
    def __init__(self, api: API):
        self.__api = api

    def get_roots(self) -> List[RootModel]:
        """
        Get all roots from the API. Roots are the top level directories that
        shade is indexing / searching from
        """
        json_response = self.__api.