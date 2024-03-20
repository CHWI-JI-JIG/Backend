import __init__
from dataclasses import dataclass
from abc import ABCMeta, abstractmethod
from typing import Optional, Self
from uuid import UUID

from Domains import ID


@dataclass(frozen=True)
class MemberID(ID):
    uuid: UUID
    sequence: int = -1

    def get_id(self) -> str:
        return self.uuid.hex


class IMemberIDBuilder(metaclass=ABCMeta):
    @abstractmethod
    def build(self) -> MemberID: ...
