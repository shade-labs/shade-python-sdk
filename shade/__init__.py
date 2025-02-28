from dataclasses import dataclass

from shade.resources.asset import Asset
from shade.resources.drive import Drive
from shade.resources.file import File
from shade.resources.share import Share
from shade.resources.workspace import Workspace
from shade.utils import Auth


@dataclass
class Shade:
    api_key: str
    remote_url: str = 'https://api.shade.inc'
    fs_url: str = 'https://fs.shade.inc'

    def __post_init__(self):
        self.auth = Auth(api_key=self.api_key, remote_url=self.remote_url, fs_url=self.fs_url)

        self.workspace = Workspace(auth=self.auth, shade=self)
        self.drive = Drive(auth=self.auth, shade=self)
        self.asset = Asset(auth=self.auth, shade=self)
        self.file = File(auth=self.auth, shade=self)
        self.share = Share(auth=self.auth, shade=self)
