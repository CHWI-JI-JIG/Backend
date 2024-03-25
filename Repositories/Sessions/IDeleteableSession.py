
import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional
from result import Result
from uuid import UUID

from Domains.Members import *
from Domains.Sessions import *


class IDeleteableSession(metaclass=ABCMeta):
    """_summary_
    세션 종류      -> owner_id
    ---------------------------
    로그인 세션    -> member id (log_member)
    product,order -> 로그인세션 (log_session)

    로그인 세션 파기 시 product,order 세션 같이 파기
    """
    @abstractmethod
    def delete_session_to_key(self, session_key: str) -> Result[bool, str]: 
        """_summary_
        session key (db에서는 id) 통해서 session 삭제 (로그아웃 시 사용예정 - session 테이블 쿼리 작성 delete) 

        Args:
            session_key (str): _description_

        Returns:
            Result[bool, str]: _description_
        """
        ...
        
    @abstractmethod
    def delete_session_to_owner_id(self, owner_id: str) -> Result[bool, str]:
        """_summary_
        log_session -> owner_id, use_count, createtime (컬럼추가되어있음)
        owner_id로 조회해서 delete하는 쿼리 작성

        Args:
            owner_id (str): _description_

        Returns:
            Result[bool, str]: _description_
        """
        ...
