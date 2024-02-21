import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional
from result import Result

from Domains.Members import Member, Privacy, PayData


class ISaveableMember(metaclass=ABCMeta):
    @abstractmethod
    def save_member(self, member: Member, privacy: Privacy, pay:PayData) -> Result[None, str]:...
        
        
            

