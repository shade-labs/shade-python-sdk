from pydantic import BaseModel, field_validator, computed_field, Field
from pathlib import Path


class RemoteFile(BaseModel):
    on_remote: bool
    local_mount_location: Path = Field(default=None, required=False)
    server_mount_location: Path = Field(default=None, required=False)

    @classmethod
    @field_validator('local_mount_location', 'server_mount_location')
    def check_mounts(cls, v, values):
        """
        If on_remote is True, then local_mount_location and server_mount_location must be set.
        """
        if values['on_remote'] and (not values['local_mount_location'] or not values['server_mount_location']):
            raise ValueError("Mount locations must be given for a remote shade instance")

    @staticmethod
    def __translate_filepath_to_local(path: Path, local_mount_location: Path, server_mount_location: Path) -> Path:
        """
        This will translate a path from the server to the local machine.
        """
        # TODO this needs to handle different platforms, mounts
        if str(path).startswith(str(server_mount_location)):
            return Path(str(path).replace(str(server_mount_location), str(local_mount_location)))
    path: Path

    @computed_field
    @property
    def local_path(self) -> Path:
        if self.on_remote:
            return self.__translate_filepath_to_local(self.path, self.local_mount_location, self.server_mount_location)
        else:
            return self.path


if __name__ == "__main__":
    data = {
        "path": "/home/user/blendfile.blend"
    }
    response = RemoteFile(**data)
    print(type(response.path))  # Should print: /mnt/remote/blendfile.blend
