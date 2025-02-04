from enum import Enum


class DriveIconType(str, Enum):
    COLOR = 'color'
    EMOJI = 'emoji'
    URL = 'url'


class DriveType(str, Enum):
    CATALOG = 'catalog'
    MAGIC = 'magic'
