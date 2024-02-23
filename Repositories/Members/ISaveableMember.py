import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional
from result import Result

from Domains.Members import Member, Privacy, MemberID


class ISaveableMember(metaclass=ABCMeta):
    @abstractmethod
    def save_member(
        self, member: Member, privacy: Privacy
    ) -> Result[MemberID, str]: ...
