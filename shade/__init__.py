from dataclasses import dataclass

from shade.resources.asset import Asset
from shade.resources.drive import Drive
from shade.resources.file import File
from shade.resources.workspace import Workspace
from shade.utils import Auth


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
