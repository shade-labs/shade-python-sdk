from dataclasses import dataclass
from shade.v2.resources.workspace import Workspace


@dataclass
class Shade:
    api_key: str
    remote_url: str = 'https://api.shade.inc'

    def __post_init__(self):
        self.workspace = Workspace(self)
