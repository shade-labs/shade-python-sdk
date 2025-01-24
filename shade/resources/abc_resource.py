import typing
from abc import ABC
from dataclasses import dataclass

from shade.utils import Auth

if typing.TYPE_CHECKING:
    from shade import Shade


@dataclass
class ABCResource(ABC):
    auth: Auth
    shade: 'Shade'
