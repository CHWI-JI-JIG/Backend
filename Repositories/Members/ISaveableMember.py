import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional
from result import Result

from Domains.Members import *


class ISaveableMember(metaclass=ABCMeta):
    @abstractmethod
    def save_member(self, member: Member, privacy: Privacy) -> Result[None, str]: ...
