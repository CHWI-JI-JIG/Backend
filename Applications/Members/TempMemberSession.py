import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional
from result import Result
from uuid import UUID
from result import Result, Err, Ok
from Domains.Members import *
from Domains.Sessions import *
from Repositories.Sessions import IUseableSession


class TempMemberSession(IUseableSession):
    def save_session(self, session: ISessionSerializeable) -> Result[None, str]:
        """_summary_

        Args:
            session (ISesseionSerializeable):

        Returns:
            Result[None, str]:
                Ok(None): Seccess
                Err(str): str is reason of error
        """
        pass

    
    def load_session(self, session_key: str) -> Result[str, str]:
        """_summary_

        Args:
            session_key (UUID): session_key is uuid.hex

        Returns:
            Result[str, str]:
                Ok(str) : session value
                Err(str) : str is seasion of error
        """
        return Ok('{"seq": "10", "member_id": "d697b39f733a426f96a13fc40c8bf061", "name": "이탁균", "role": "buyer"}')
