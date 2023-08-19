from pathlib import Path

from shade import ShadeRemote

# # Where the mount point exists on my computer
# LOCAL_MOUNT_POINT = Path("/Volumes/studio")
# # Where the mount point exists on my remote server
# REMOTE_MOUNT_POINT = Path("/media/shade/Studio Drive")
# # The IP of my remote server
# SERVER_IP = 'http://192.168.196.130'


# Where the mount point exists on my computer
LOCAL_MOUNT_POINT = Path("/Volumes/studio")
# Where the mount point exists on my remote server
REMOTE_MOUNT_POINT = Path("/media/shade/Studio Drive")
# The IP of my remote server
SERVER_IP = 'http://0.0.0.0'

if __name__ == '__main__':
    shade = ShadeRemote(
        LOCAL_MOUNT_POINT,
        REMOTE_MOUNT_POINT,
        SERVER_IP
    )

    print(shade.get_assets())
