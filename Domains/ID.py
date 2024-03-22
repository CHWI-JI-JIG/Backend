from dataclasses import dataclass
from abc import ABCMeta, abstractmethod
from typing import Optional, Self, Union
from result import Result, Ok, Err
from uuid import UUID, uuid4

from Commons.helpers import check_hex_string


class ID(metaclass=ABCMeta):
    @abstractmethod
    def get_id(self) -> str: ...
    # @abstractmethod
    # def get_seq(self) -> Optional[int]: ...


class IIDBuilder(metaclass=ABCMeta):
    @abstractmethod
    def set_seqence(self, seq: int) -> Self: ...

    @abstractmethod
    def set_uuid(self, uuid_hex: Optional[str] = None) -> Result[Self, str]: ...


class IDBuilder(IIDBuilder):
    def __init__(self):
        self.uuid: Optional[UUID] = None
        self.sequence: Optional[int] = None

    def set_seqence(self, seq: int) -> Self:
        assert isinstance(seq, int), "Type of seq is int."
        assert self.sequence is None, "The sequence is already set."
        assert seq >= 0, "seq >= 0"

        self.sequence = seq
        return self

    def set_uuid(self, uid: Union[UUID, str, None] = None) -> Result[Self, str]:
        assert self.uuid is None, "The uuid_hex is already set."
        match uid:
            case None:
                self.uuid = uuid4()
            case k if isinstance(uid, str):
                assert check_hex_string(k), "The uuid_hex is not in hex format."
                if not check_hex_string(k):
                    return Err("not hex format")
                try:
                    self.uuid = UUID(hex=uid)
                except:
                    return Err("Not Convert UUID")
            case id if isinstance(id, UUID):
                self.uuid = id
            case _:
                assert False, "Type of uuid_hex is str."

        return Ok(self)
    
