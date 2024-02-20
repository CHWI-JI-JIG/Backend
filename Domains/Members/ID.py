from dataclasses import dataclass
from abc import ABCMeta, abstractmethod
from typing import Optional, Self
from uuid import uuid4, UUID


class ID(metaclass=ABCMeta):
    @abstractmethod
    def get_id(self) -> str: ...


class MemberID(metaclass=ABCMeta): ...


@dataclass(frozen=True)
class MemberUUID(MemberID):
    sequence: int = -1
    uuid: UUID

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
