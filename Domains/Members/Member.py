import __init__
from dataclasses import dataclass
from abc import ABCMeta, abstractmethod
from typing import Optional, Self
from enum import Enum

from Domains.Members import MemberID


class RuleType(Enum):
    SELLER = "seller"
    BUYER = "buyer"
    ADMIN = "admin"

    def __str__(self):
        return str(self.value)


@dataclass(frozen=True)
class Member:
    id: MemberID
    account: str
    passwd: str
    rule: RuleType


class IMemberBuilder(metaclass=ABCMeta):
    @abstractmethod
    def set_id(self, id: MemberID) -> Self: ...

    @abstractmethod
    def set_account(self, account: str) -> Self: ...

    @abstractmethod
    def set_passwd(self, passwd: str) -> Self: ...

    @abstractmethod
    def set_rule(self, rule: RuleType) -> Self: ...

    @abstractmethod
    def build(self) -> Member: ...
