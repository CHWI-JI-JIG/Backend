import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional
from result import Result
from uuid import UUID

from Domains.Members import *
from Domains.Sessions import *


class IMakeSaveMemberSession(metaclass=ABCMeta):
    @abstractmethod
    def make_and_save_session(self,member_id:MemberID) -> Result[MemberSession, str]:
        """
        Read User table. Make MemberSession. Save MemberSession

        Returns:
            Result[MemberSession, str]:
                Ok(member_session): Sucess to Save memberSession
                Err(e) : db Error
        """
        ...
