import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional, List
from result import Result
from uuid import UUID

from Domains.Members import *
from Domains.Sessions import *


class ILoadableSession(metaclass=ABCMeta):
    @abstractmethod
    def load_session(self, session_key: str) -> Result[SessionToken, str]:
        """_summary_

        Args:
            session_key (UUID): session_key is uuid.hex

        Returns:
            Result[str, str]:
                Ok(SessionToken) : session token
                Err(str) : str is seasion of error
        """
        ...
    
    @abstractmethod
    def load_session_from_owner_id(self, owner_id: str) -> Result[List[SessionToken], str]:
        """_summary_
        owner_id로 조회하는 코드 (여러개 존재 가능)

        Args:
            owner_id

        Returns:
            Result[str, str]:
                Ok(SessionToken) : session token
                Err(str) : str is seasion of error
        """
        ...
    
