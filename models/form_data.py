from dataclasses import dataclass


@dataclass
class FormData:
    name: str
    email: str
    message: str