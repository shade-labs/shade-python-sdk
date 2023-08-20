import requests
from shade.v1.routes.roots import Roots
from shade.v1.api import API
from pathlib import Path
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


class ShadeLocal(__Shade):
    """
    A local instance to connect to. This will do no filepath translation.
    """
    def __init__(self, ip: str = 'http://127.0.0.0', port: int = 9082):
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