import os
from pathlib import Path
from typing import Dict

from pydantic import BaseModel, model_validator


# TODO this needs to optimized a ton
class MountInfo(BaseModel):
    local_mount_location: Path  # Where the mount point exists on my computer
    server_mount_location: Path  # Where the mount point exists on my remote server

    def translate_filepath_to_local(self, path: Path) -> Path:
        """
        This will translate a path from the server to the local machine.
        TODO handle UNC and Windows paths
        """
        return path
        # # Normalize paths to have the appropriate slash depending on the OS
        # normalized_path = str(path).replace('/', os.sep).replace('\\', os.sep)
        # normalized_server_mount = str(self.server_mount_location).replace('/', os.sep).replace('\\', os.sep)
        # normalized_local_mount = str(self.local_mount_location).replace('/', os.sep).replace('\\', os.sep)
        #
        # # Consider case insensitivity (primarily for Windows)
        # if Path(normalized_path).drive or normalized_path.startswith('\\\\'):
        #     # We're on Windows or dealing with a UNC path
        #     normalized_path = normalized_path.lower()
        #     normalized_server_mount = normalized_server_mount.lower()
        #
        # if normalized_path.startswith(normalized_server_mount):
        #     # Replace the server mount with the local mount
        #     translated_path = normalized_path.replace(normalized_server_mount, normalized_local_mount, 1)
        #     # Return the resolved path (normalizing any .. or .)
        #     return Path(translated_path).resolve()
        # else:
        #     # If the path doesn't start with the server mount, return the original path
        #     return path

    def translate_filepath_to_server(self, path: Path) -> Path:
        """
        This will translate a path from the local machine to the server's perspective.
        """
        return path
        # # Normalize paths to have the appropriate slash depending on the OS
        # normalized_path = str(path).replace('/', os.sep).replace('\\', os.sep)
        # normalized_server_mount = str(self.server_mount_location).replace('/', os.sep).replace('\\', os.sep)
        # normalized_local_mount = str(self.local_mount_location).replace('/', os.sep).replace('\\', os.sep)
        #
        # # Consider case insensitivity (primarily for Windows)
        # if Path(normalized_path).drive or normalized_path.startswith('\\\\'):
        #     # We're on Windows or dealing with a UNC path
        #     normalized_path = normalized_path.lower()
        #     normalized_local_mount = normalized_local_mount.lower()
        #
        # if normalized_path.startswith(normalized_local_mount):
        #     # Replace the local mount with the server mount
        #     translated_path = normalized_path.replace(normalized_local_mount, normalized_server_mount, 1)
        #     # Return the resolved path (normalizing any .. or .)
        #     return Path(translated_path).resolve()
        # else:
        #     # If the path doesn't start with the local mount, return the original path
        #     return path


class ServerResponse(BaseModel):
    local_path: Path
    remote_path: Path

    mount_info: MountInfo

    @model_validator(mode='before')
    @classmethod
    def translate_file_path(cls, data: Dict):
        """
        If on_remote is True, then local_mount_location and server_mount_location must be set.
        """
        if 'path' in data:
            data['local_path'] = data['mount_info'].translate_filepath_to_local(Path(data['path']))

            data['remote_path'] = Path(data['path'])

            del data['path']

            data['mount_info'] = data['mount_info']

        return data


class LocalToRemote(BaseModel):
    pass



if __name__ == "__main__":
    data_ = {
        "path": "/home/user/blendfile.blend",
        "mount_info": MountInfo(local_mount_location=Path('/Volumes/studio'), server_mount_location=Path('/home/user'))
    }
    response = ServerResponse(**data_)
    print(response.local_path)  # Should print: /mnt/remote/blendfile.blend
