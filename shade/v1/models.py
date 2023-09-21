import enum
import uuid
from datetime import datetime
from enum import Enum
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from dataclass_wizard import asdict
from pydantic import BaseModel
from pydantic import validator


class License(Enum):
    """Asset Licenses"""
    CC_BY = 'cc-by'
    CC_BY_SA = 'cc-by-sa'
    CC_BY_ND = 'cc-by-nd'
    CC_BY_NC = 'cc-by-nc'
    CC_BY_NC_SA = 'cc-by-nc-sa'
    CC_BY_NC_ND = 'cc-by-nc-nd'
    CC0 = 'cc0'
    UNKNOWN = 'unknown'
    OTHER = 'other'


class AssetType(Enum):
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
    SEQUENCE = "SEQUENCE"
    AFTER_EFFECTS = 'AFTER_EFFECTS'
    MOGRT = 'MOGRT'
    ILLUSTRATOR = 'ILLUSTRATOR'
    EXR = 'EXR'
    DOCUMENT = 'DOCUMENT'
    # frontend stock assets are sometimes saved as such?
    # TODO investigate this, added to fix:
    #  https://discord.com/channels/984951878192353321/1096557388095570031/1126296508560584775
    STOCK = 'STOCK'
    OTHER = 'OTHER'


class CollectionType(enum.Enum):
    AUTO = 'auto'
    USER = 'user'


class IndexingQueueItem(BaseModel):
    path: str
    working: bool


class IndexingStatus(Enum):
    IDLE = 'IDLE'
    INDEXING = 'INDEXING'
    DOWNLOADING = 'DOWNLOADING'


class StatusResponse(BaseModel):
    progress: int
    total: int
    last_synced: Optional[datetime]
    state: IndexingStatus
    paused: bool


class RootModel(BaseModel):
    id: uuid.UUID
    path: str
    created: datetime
    updated: datetime
    files_found: int = 0
    size_bytes: int = 0

    # TODO make these all computed fields pending our update to pydantic 2.0

    is_directory: bool = False

    ctime: Optional[datetime] = None
    mtime: Optional[datetime] = None


def dataclass_to_dict(v: Any):
    """Converts a Dataclass to a dictionary, to return to the client"""
    if v is None:
        return None
    if isinstance(v, dict):
        return v
    try:
        return asdict(v)
    except TypeError:
        raise ValueError(f"Invalid type for field: {type(v)}")


class CommentModel(BaseModel):
    id: uuid.UUID
    content: str

    created: datetime
    updated: datetime


class AssetComments(BaseModel):
    """Comments for an asset"""
    asset_id: uuid.UUID
    comments: List[CommentModel]


class PreviewModel(BaseModel):
    id: uuid.UUID
    path: str
    thumbnail: str
    created: datetime


class AssetModel(BaseModel):
    id: uuid.UUID
    name: str
    user_description: Optional[str]
    description: str

    signature: int

    updated: datetime
    created: datetime
    file_created: Optional[datetime]
    file_modified: Optional[datetime]

    timestamp: int = None

    path: str
    type: AssetType
    tags: List[str]

    size_bytes: int

    source: List[str]

    objects: List[object]
    transcription: Optional[str]
    rating: Optional[float]
    blurhash: str
    palette: List[List[int]]
    ocr: Optional[str]
    category: Optional[str]
    extension: str
    license: License
    asset_metadata: dict
    preview_images: List[PreviewModel]

    texture_data: Optional[dict]
    _texture_data_validator = validator('texture_data', pre=True, allow_reuse=True)(dataclass_to_dict)

    integration_data: Optional[dict]
    _integration_data_validator = validator('integration_data', pre=True, allow_reuse=True)(dataclass_to_dict)

    proxy_path: Optional[str]
    ai_indexed: bool

    comments: List[CommentModel]


class CollectionModel(BaseModel):
    id: uuid.UUID
    name: str
    description: str
    type: CollectionType
    tags: List[str]
    filters: Dict[str, List[str]]
    preview_asset: Optional[AssetModel]

    # TODO: use computed_field for pydantic v2
    preview_image: Optional[PreviewModel]


class CollectionModelWithAssets(CollectionModel):
    assets: List[AssetModel]
    manually_added_assets: List[AssetModel]
    autogenerated_assets: List[AssetModel] = []