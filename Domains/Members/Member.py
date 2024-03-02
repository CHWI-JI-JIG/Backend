import __init__
from dataclasses import dataclass
from abc import ABCMeta, abstractmethod
from typing import Optional, Self
from enum import Enum

from Domains.Members import MemberID


class RoleType(Enum):
    SELLER = "seller"
    BUYER = "buyer"
    ADMIN = "admin"

    def __str__(self):
        return str(self.value)


@dataclass(frozen=True)
class Member:
    id: MemberID
    account: str
    role: RoleType
    passwd: Optional[str] = None


class IMemberBuilder(metaclass=ABCMeta):
    @abstractmethod
    def set_id(self, id: MemberID) -> Self: ...

    @abstractmethod
    def set_account(self, account: str) -> Self: ...

    @abstractmethod
    def set_passwd(self, passwd: str) -> Self: ...

    @abstractmethod
    def set_role(self, role: RoleType) -> Self: ...

    @abstractmethod
    def build(self) -> Member: ...
