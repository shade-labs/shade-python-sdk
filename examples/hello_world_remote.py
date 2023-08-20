from pathlib import Path

from shade import ShadeRemote

# # Where the mount point exists on my computer
# LOCAL_MOUNT_POINT = Path("/Volumes/studio")
# # Where the mount point exists on my remote server
# REMOTE_MOUNT_POINT = Path("/media/shade/Studio Drive")
# # The IP of my remote server
# SERVER_IP = 'http://192.168.196.130'


# Where the mount point exists on my computer
LOCAL_MOUNT_POINT = Path("/")
# Where the mount point exists on my remote server
REMOTE_MOUNT_POINT = Path("/")
# The IP of my remote server
SERVER_IP = 'http://0.0.0.0'

if __name__ == '__main__':
    server = ShadeRemote(
        LOCAL_MOUNT_POINT,
        REMOTE_MOUNT_POINT,
        SERVER_IP
    )

    print(server.roots.get_roots())
    roots = []
    for i in range(10):
        print(server.roots.add_new_root(Path('/home/shade/Downloads')))

    print(server.roots.get_roots())

    for root in server.roots.get_roots():
        server.roots.delete_root(root.id)

    print(server.roots.get_roots())
