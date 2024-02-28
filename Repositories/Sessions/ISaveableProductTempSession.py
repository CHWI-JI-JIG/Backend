import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional
from result import Result
from uuid import UUID

from Domains.Members import *
from Domains.Sessions import *


class ISaveableProductTempSession(metaclass=ABCMeta):
    @abstractmethod
    def upload_or_save_product_temp_session(
        self, session: ProductTempSession
    ) -> Result[ProductTempSession, str]:
        """
        Read User table. Make MemberSession. Save MemberSession

        Returns:
            Result[MemberSession, str]:
                Ok(member_session): Sucess to Save memberSession
                Err(e) : db Error
        """
        ...
