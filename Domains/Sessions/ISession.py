import __init__
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Self, Optional, Union
from result import Result, Err, Ok
from uuid import UUID, uuid4
from datetime import datetime

from Commons.helpers import check_hex_string
from Commons.format import KOREA_TIME_FORMAT
from icecream import ic


@dataclass(frozen=True)
class SessionToken:
    key : str
    value: str
    owner_id: str
    create_time: datetime
    use_count: int


@dataclass(frozen=True)
class SecuritySession(metaclass=ABCMeta):
    key: UUID
    owner_id: UUID
    create_time: datetime
    use_count: int

    def get_key(self) -> str:
        return self.key.hex

    def get_owner_id(self) -> str:
        return self.owner_id.hex

    def get_create_time(self) -> datetime:
        return self.create_time

    def get_use_count(self) -> int:
        return self.use_count
    
    @abstractmethod
    def MAX_USE_COUNT(self)->int:...
    
    @abstractmethod
    def VALIDE_MINUTE(self)->int:...


class SecuritySessionBuilder:
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

    def set_owner_id(self, owner_id: Union[UUID, str]) -> Result[Self, str]:
        assert self.owner_id is None, "The owner is already set."

        if isinstance(owner_id, str):
            if not check_hex_string(owner_id):
                return Err("The owner_id is not in hex format.")
            try:
                self.owner_id = UUID(hex=owner_id)
            except:
                return Err("Not Convert UUID")
        elif isinstance(owner_id, UUID):
            self.owner_id = owner_id
        else:
            assert False, "Type of owner_id is hex or UUID"
        assert isinstance(self.owner_id, UUID), "Type of owner_id is UUID"
        return Ok(self)

    def set_use_count(self, count: Optional[int] = None) -> Self:
        assert self.use_count is None, "use_count is already set."
        if count is None:
            count = 0
        assert count >= 0, "Use count must be a non-negative integer."
        self.use_count = count
        return self

    def set_create_time(self, time: Union[datetime, str, None] = None) -> Self:
        assert self.create_time is None, "create_time is already set."
        if time is None:
            time = datetime.now().replace(microsecond=0)
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

        return Ok(self)

    def assert_and_check_about_setting(self) -> bool:
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


class ISucuritySessionGetable(metaclass=ABCMeta):
    @abstractmethod
    def get_id(self) -> str: ...

    @abstractmethod
    def get_owner_id(self) -> str: ...

    @abstractmethod
    def get_create_time(self) -> datetime: ...

    @abstractmethod
    def get_use_count(self) -> int: ...


class ISessionSerializeable(metaclass=ABCMeta):
    @abstractmethod
    def serialize_key(self) -> str: ...

    @abstractmethod
    def serialize_value(self) -> str: ...


class ISessionBuilder(metaclass=ABCMeta):
    @abstractmethod
    def set_deserialize_key(self, key: str) -> Self: ...

    @abstractmethod
    def set_deserialize_value(self, token: SessionToken) -> Result[Self, str]: ...


def make_session_token(token_builder: ISessionSerializeable) -> SessionToken:
    # assert isinstance(
    #     token_builder, ISessionSerializeable
    # ), "Parent of token_builder is ISessionBuilder."
    # assert isinstance(
    #     token_builder, SecuritySession
    # ), "Parent of token_builder is SecuritySession."
    assert issubclass(
        type(token_builder), ISessionSerializeable
    ), "token_builder must inherit from ISessionSerializeable"
    assert issubclass(
        type(token_builder), SecuritySession
    ), "token_builder must inherit from SecuritySession"

    return SessionToken(
        key=token_builder.serialize_key(),
        value=token_builder.serialize_value(),
        owner_id=token_builder.get_owner_id(),
        create_time=token_builder.get_create_time(),
        use_count=token_builder.get_use_count(),
    )
