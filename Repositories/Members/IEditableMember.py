import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional
from result import Result

from Domains.Members import *


class IEditableMember(metaclass=ABCMeta):
    @abstractmethod
    def update_role(self, member_id: MemberID, role:RoleType) -> Result[MemberID, str]: ...

    # @abstractmethod
    # def delete_member(self, member_id: MemberID) -> Result[MemberID, str]: ...
