import __init__
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Self, Optional,Union
from result import Result, Err, Ok
from uuid import UUID, uuid4
from datetime import datetime

from Commons.helpers import check_hex_string
from Commons.format import KOREA_TIME_FORMAT


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

    def set_owner_id(self, owner_id: str) -> Result[Self, str]:
        assert isinstance(owner_id, str), "Type of owner_id is hex"
        if not check_hex_string(owner_id):
            return Err("The owner_id is not in hex format.")
        try:
            self.owner_id = UUID(hex=owner_id)
        except:
            return Err("Not Convert UUID")
        return Ok(self)

    def set_use_count(self, count: Optional[int] = None) -> Self:
        if count is None:
            count = 0
        assert count < 0, "Use count must be a non-negative integer."
        self.use_count = count
        return self

    def set_create_time(self, time: Union[datetime, str, None] = None) -> Self:
        # write code
        if time is None:
            time = datetime.now()
        elif isinstance(time, str):
            try:
                time = datetime.strptime(time, KOREA_TIME_FORMAT)
            except:
                assert False, f"Format of time(str) is ({KOREA_TIME_FORMAT})"
        assert isinstance(time, datetime), "Type of time is datetime"
        self.create_time = time
        return self

    def set_key(self, key: Optional[str] = None) -> Result[Self, str]:
        assert self.key is None, "The Key is already set."
        match key:
            case None:
                self.key = uuid4()
            case k if isinstance(key, str):
                assert check_hex_string(k), "The uuid_hex is not in hex format."
                if not check_hex_string(k):
                    return Err("The uuid_hex is not in hex format.")
                try:
                    self.key = UUID(hex=key)
                except:
                    return Err("Not Convert UUID")
            case _:
                assert False, "Type of key is str."

        return Result(self)
    
    def assert_and_check_about_setting(self)->bool:
        if not isinstance(self.key, UUID):
            assert False, "You didn't set the key."
            return False
        if not isinstance(self.owner_id, UUID):
            assert False, "You didn't set the owner_id."
            return False
        if not isinstance(self.use_count, int):
            assert False, "You didn't set the use_count."
            return False
        if not isinstance(self.create_time, datetime):
            assert False, "You didn't set the create_time."
            return False
        return True
        
        


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
