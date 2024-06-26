import __init__
from dataclasses import dataclass
from abc import ABCMeta, abstractmethod
from typing import Optional, Self
from datetime import datetime

from Commons.format import KOREA_TIME_FORMAT
from Domains.Members import MemberID, RoleType


@dataclass(frozen=True)
class Authentication:
    id: MemberID
    last_changed_date: datetime
    last_access: datetime
    fail_count: int
    role: RoleType
    is_sucess: bool

    def str_last_access(self) -> str:
        assert isinstance(self.last_access, datetime), "Type of last_access is datetime"
        time = self.last_access.strftime(KOREA_TIME_FORMAT)
        return time


class IAuthenticationBuilder(metaclass=ABCMeta):
    @abstractmethod
    def set_id(self, id: MemberID) -> Self: ...

    @abstractmethod
    def set_last_access(self, time: datetime) -> Self: ...

    @abstractmethod
    def set_last_changed_date(self, time: datetime) -> Self: ...

    @abstractmethod
    def set_fail_count(self, cnt: int) -> Self: ...
    
    @abstractmethod
    def set_role(self, role: RoleType) -> Self: ...

    @abstractmethod
    def build(self) -> Authentication: ...
