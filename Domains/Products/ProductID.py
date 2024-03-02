import __init__
from dataclasses import dataclass
from abc import ABCMeta, abstractmethod
from typing import Optional, Self
from uuid import UUID

from Domains import ID


@dataclass(frozen=True)
class ProductID(ID):
    uuid: UUID
    sequence: int = -1

    def get_id(self) -> str:
        return self.uuid.hex


class IProductIDBuilder(metaclass=ABCMeta):
    @abstractmethod
    def set_seqence(self, seq: int) -> Self: ...

    @abstractmethod
    def set_uuid(self, uuid_hex: Optional[str] = None) -> Self: ...

    @abstractmethod
    def build(self) -> ProductID: ...
