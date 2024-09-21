from abc import ABC
from dataclasses import dataclass
from shade.v2.utils import Auth


@dataclass
class ABCResource(ABC):
    auth: Auth
