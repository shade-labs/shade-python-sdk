"""Note: All these values/enums are copied from Shade API"""

from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel


class DriveIconType(str, Enum):
    COLOR = 'color'
    EMOJI = 'emoji'
    URL = 'url'


class DriveType(str, Enum):
    CATALOG = 'catalog'
    MAGIC = 'magic'


class MetadataAttributeType(str, Enum):
    STRING = 'str'
    SINGLE_SELECT = 'single_select'
    MULTI_SELECT = 'multi_select'
    FLOAT = 'float'
    INTEGER = 'int'
    BOOLEAN = 'bool'
    DATE = 'datetime'
    RATING = 'rating'


class MetadataAttributeSelectOptionColor(str, Enum):
    PINK = 'pink'
    RED = 'red'
    YELLOW = 'yellow'
    LIGHT_GREEN = 'light_green'
    DARK_GREEN = 'dark_green'
    LIGHT_BLUE = 'light_blue'
    DARK_BLUE = 'dark_blue'
    PURPLE = 'purple'


class MetadataAttributeSelectOption(BaseModel):
    id: str
    name: str
    color: MetadataAttributeSelectOptionColor
    user: bool


class AssetType(str, Enum):
    IMAGE = 'IMAGE'
    VIDEO = 'VIDEO'
    AUDIO = 'AUDIO'
    OBJECT = 'OBJECT'
    MAYA = 'MAYA'
    NUKE = 'NUKE'
    MAX = 'MAX'
    HDR = 'HDR'
    HDRI = 'HDRI'
    BLENDER = 'BLENDER'
    HOUDINI = 'HOUDINI'
    PHOTOSHOP = 'PHOTOSHOP'
    UNREAL = 'UNREAL'
    UNITY = 'UNITY'
    TEXTURE = 'TEXTURE'
    SEQUENCE = 'SEQUENCE'
    AFTER_EFFECTS = 'AFTER_EFFECTS'
    MOGRT = 'MOGRT'
    ILLUSTRATOR = 'ILLUSTRATOR'
    EXR = 'EXR'
    DOCUMENT = 'DOCUMENT'
    STOCK = 'STOCK'
    OTHER = 'OTHER'


class MetadataAttribute(BaseModel):
    id: str  # uuid for the attribute a user creates
    name: str  # name the user provides
    keys: list[str]
    value_type: MetadataAttributeType
    description: str  # user provided description
    location: str = 'custom'
    default: Optional[Any] = None  # ignore
    group: Optional[str] = None  # ignore
    options: Optional[list[MetadataAttributeSelectOption]] = (
        None  # used for select and multi-select
    )
    add_new_options: Optional[bool] = (
        True  # True allows GPT to create new options outside the current set
    )
    restrict_to_types: Optional[list[AssetType]] = None
    automated: Optional[bool] = False  # true if we need to send to GPT
    prompt: Optional[str] = None  # prompt for an automated attribute
    archived: Optional[bool] = False  # don't run jobs on archived attributes
