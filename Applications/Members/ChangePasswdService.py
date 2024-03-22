import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional, Tuple, List
from result import Result, Ok, Err

from uuid import uuid4, UUID

from Domains.Members import *
from Domains.Sessions import *
from Builders.Members import *
from Repositories.Members import *
from Applications.Members.ExtentionMethod import hashing_passwd
from datetime import datetime, timedelta
from Repositories.Sessions import IMakeSaveMemberSession

from icecream import ic


class ChangePasswdService:
    def __init__(
        self,
        pass_repo: IChangeablePasswd,
        session_repo: IMakeSaveMemberSession,
    ):
        assert issubclass(
            type(pass_repo), IChangeablePasswd
        ), "auth_member_repo must be a class that inherits from  IChangeablePasswd."

        self.pass_repo = pass_repo
        self.session_repo = session_repo

    def change_pw_on_nologin(
        self,
        passwd: str,
        account: str,
        page_session: str,
    ) -> Result[MemberSession, str]:
        # TODO
        # 일단은 패스
        ...

    def change_expired_pw(
        self,
        new_passwd: str,
        old_passwd: str,
        user_key: str,
    ) -> Result[MemberSession, str]:
        # TODO
        # 유저 세션 검증
        # old pw 맞는지 점검
        # 새 pw 업데이트
        ...
