from Domains.Members import MemberID
import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional, Tuple, List
from result import Result, Ok, Err

from uuid import uuid4, UUID


from Domains.Sessions import *
from datetime import datetime, timedelta
from Repositories.Sessions import IDeleteableSession

from icecream import ic


class MemberSessionService:
    def __init__(
        self,
        del_session_repo : IDeleteableSession,
    ):
        assert issubclass(
            type(del_session_repo), IDeleteableSession
        ), "del_session_repo must be a class that inherits from IDeleteableSession."

        self.del_repo = del_session_repo
 
    
    def logout(self, user_key:str)-> bool:
        # 1. member session 만료 (삭제)
        del_session_result = self.del_repo.delete_session_to_key(user_key)
        if del_session_result.is_err():
            return False
        
        # 2. owner_id가 멤버 세션인 세션 삭제
        del_owner_session_result = self.del_repo.delete_session_to_owner_id(user_key)
        if del_owner_session_result.is_err():
            return False

        return True

    
    def find_login_session(self, member_id:MemberID)->  Result[List[SessionToken], str]:
        ...
    