import __init__
from dataclasses import dataclass
from abc import *
from typing import Optional, Self

from Domains.Members import MemberID


@dataclass(frozen=True)
class Member:
    id: MemberID
    account: str
    passwd: str


class IMemberBuilder(metaclass=ABCMeta):
    @abstractmethod
    def set_id(self, id: MemberID) -> Self: ...

    @abstractmethod
    def set_account(self, account: str) -> Self: ...

    @abstractmethod
    def set_passwd(self, passwd: str) -> Self: ...

    @abstractmethod
    def build(self) -> Member: ...
