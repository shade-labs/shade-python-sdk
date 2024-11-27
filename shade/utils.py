from dataclasses import dataclass


@dataclass
class Auth:
    api_key: str
    remote_url: str = 'https://api.shade.inc'
