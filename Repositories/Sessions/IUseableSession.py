import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional
from result import Result
from uuid import UUID

from Domains.Members import *
from Domains.Sessions import *


class IUseableSession(metaclass=ABCMeta):
    @abstractmethod
    def save_session(self, session: ISessionSerializeable) -> Result[UUID, str]:
        """_summary_

        Args:
            session (ISesseionSerializeable):

        Returns:
            Result[None, str]:
                Ok(None): Seccess
                Err(str): str is reason of error
        """
        ...

    @abstractmethod
    def load_session(self, session_key: str) -> Result[str, str]:
        """_summary_

        Args:
            session_key (UUID): session_key is uuid.hex

        Returns:
            Result[str, str]:
                Ok(str) : session value
                Err(str) : str is seasion of error
        """
        ...
