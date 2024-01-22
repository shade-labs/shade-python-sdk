from pathlib import Path

from shade.v1.api import API
from shade.v1.routes.assets import Assets
from shade.v1.routes.config import Config
from shade.v1.routes.convert import Convert
from shade.v1.routes.indexing import Indexing
from shade.v1.routes.models import Models
from shade.v1.routes.previews import Previews
from shade.v1.routes.roots import Roots
from shade.v1.routes.search import Search
from shade.v1.routes.server import Server
from shade.v1.types import MountInfo


class __Shade:
    mount_info: MountInfo
    ip: str
    port: int

    def __init__(self, local_mount_location: Path, server_mount_location: Path, ip: str, port: int):
        self.mount_info = MountInfo(
            local_mount_location=local_mount_location,
            server_mount_location=server_mount_location
        )
        self.ip = ip
        self.port = port

        self.__api = API(f'{self.ip}:{self.port}')
        self.roots = Roots(self.__api, self.mount_info)
        self.previews = Previews(self.__api, self.mount_info)
        self.indexing = Indexing(self.__api, self.mount_info)
        self.config = Config(self.__api, self.mount_info)
        self.assets = Assets(self.__api, self.mount_info)
        self.search = Search(self.__api, self.mount_info)
        self.server = Server(self.__api, self.mount_info)
        self.convert = Convert(self.__api, self.mount_info)
        self.models = Models(self.__api, self.mount_info)


class ShadeLocal(__Shade):
    """
    A local instance to connect to. This will do no filepath translation.
    """
    def __init__(self, ip: str = 'http://localhost', port: int = 9082):
        super().__init__(
            Path('/'),
            Path('/'),
            ip,
            port
        )


class ShadeRemote(__Shade):
    """
    This must perform filepath translation.

    For example a blender file on the remote server may be at
    /home/user/blendfile.blend

    But on the local machine it may be at
    /mnt/remote/home/user/blendfile.blend

    This constructor will take in the path it is on the machine which is
    /mnt/remote/home/user/blendfile.blend

    and translate those to server calls like
    /home/user/blendfile.blend
    """
    def __init__(self, local_mount_location: Path, server_mount_location: Path, ip: str, port: int = 9082):
        super().__init__(
            local_mount_location,
            server_mount_location,
            ip,
            port
        )
