from dataclasses import dataclass

from shade.v2.resources.asset import Asset
from shade.v2.resources.drive import Drive
from shade.v2.resources.file import File
from shade.v2.resources.workspace import Workspace
from shade.v2.utils import Auth


@dataclass
class Shade:
    api_key: str
    remote_url: str = 'https://api.shade.inc'

    def __post_init__(self):
        self.auth = Auth(api_key=self.api_key, remote_url=self.remote_url)
        self.workspace = Workspace(auth=self.auth)
        self.drive = Drive(auth=self.auth)
        self.asset = Asset(auth=self.auth)
        self.file = File(auth=self.auth)
