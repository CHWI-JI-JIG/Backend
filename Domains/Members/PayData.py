import __init__
from dataclasses import dataclass
from abc import ABCMeta, abstractmethod
from typing import Optional, Self, List, Union
from enum import Enum

from Domains.Members import MemberID


@dataclass
class PayData:
    id: MemberID
    pay_account_list: List[str]


class IPayDataBuilder(metaclass=ABCMeta):
    @abstractmethod
    def set_id(self, id: MemberID) -> Self: ...

    @abstractmethod
    def add_pay_account(self, pay_account: Union[List[str], str]) -> Self: ...

    @abstractmethod
    def build(self) -> PayData: ...
