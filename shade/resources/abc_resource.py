from abc import ABC
from dataclasses import dataclass

from shade.utils import Auth


@dataclass
class ABCResource(ABC):
    auth: Auth
