from dataclasses import dataclass
from abc import ABCMeta, abstractmethod
from typing import Optional, Self
from uuid import uuid4, UUID


@dataclass(frozen=True)
class MemberID:
    uuid: UUID
    sequence: int = -1

    def get_id(self) -> str:
        return self.uuid.hex


class IMemberIDBuilder(metaclass=ABCMeta):
    @abstractmethod
    def set_seqence(self, seq: int) -> Self: ...

    @abstractmethod
    def set_uuid4(self) -> Self: ...

    @abstractmethod
    def set_uuid_hex(self, uuid_hex: str) -> Self: ...

    @abstractmethod
    def build(self) -> MemberID: ...
