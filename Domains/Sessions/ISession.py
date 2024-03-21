import __init__
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Self, Optional
from result import Result
from uuid import UUID, uuid4
from datetime import datetime

from Commons.helpers import check_hex_string


@dataclass(frozen=True)
class SecuritySession:
    key: UUID
    owner_id: UUID
    create_time: datetime
    use_count: int


class SecuritySessionBuilder:
    # TODO
    def __init__(
        self,
        key: Optional[UUID] = None,
        owner_id: Optional[UUID] = None,
        use_count: Optional[int] = None,
        create_time: Optional[datetime] = None,
    ):
        self.key = key
        self.owner_id = owner_id
        self.use_count = use_count
        self.create_time = create_time

    def set_owner_id(self, owner_id:str) -> Self:
        # TODO
        return self

    def set_key(self, key: Optional[str] = None) -> Self:
        assert self.key is None, "The Key is already set."
        match key:
            case None:
                self.key = uuid4()
            case k if isinstance(key, str):
                assert check_hex_string(k), "The uuid_hex is not in hex format."
                self.key = UUID(hex=key)
            case _:
                assert False, "Type of key is str."

        return self


class ISessionSerializeable(metaclass=ABCMeta):
    @abstractmethod
    def serialize_key(self) -> str: ...

    @abstractmethod
    def serialize_value(self) -> str: ...


class ISesseionBuilder(metaclass=ABCMeta):
    @abstractmethod
    def set_deserialize_key(self, key: str) -> Self: ...

    @abstractmethod
    def set_deserialize_value(self, value: str) -> Result[Self, str]: ...
