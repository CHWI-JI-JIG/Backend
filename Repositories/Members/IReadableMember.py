import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional, Tuple, List
from result import Result

from Domains.Members import *


class IReadableMember(metaclass=ABCMeta):
    # @abstractmethod
    # def check_exist_account(self, account: str) -> bool: ...

    # @abstractmethod
    # def get_member(self, member_id: MemberID) -> Result[Member, str]: ...

    @abstractmethod
    def get_privacy(self, member_id: MemberID) -> Result[Privacy, str]: ...

    # @abstractmethod
    # def get_member_and_privacy(
    #     self, member_id: MemberID
    # ) -> Result[Tuple[Member, Privacy], str]: ...
