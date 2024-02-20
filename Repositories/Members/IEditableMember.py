import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional
from result import Result

from Domains.Members import *


class IEditableMember(metaclass=ABCMeta):
    @abstractmethod
    def update_member(self, member: Member, privacy: Privacy) -> Result[None, str]: ...

    @abstractmethod
    def delete_member(self, member_id: MemberID) -> Result[None, str]: ...
