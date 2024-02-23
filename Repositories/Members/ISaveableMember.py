import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional
from result import Result
from uuid import UUID

from Domains.Members import Member, Privacy, Authentication


class ISaveableMember(metaclass=ABCMeta):
    @abstractmethod
    def save_member(self, member: Member, privacy: Privacy) -> Result[UUID, str]: ...
