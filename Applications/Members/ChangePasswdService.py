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
from Repositories.Sessions import *

from icecream import ic


class ChangePasswdService:
    def __init__(
        self,
        pass_repo: IChangeablePasswd,
        load_session_repo: ILoadableSession,
        # make_session_repo: IMakeSaveMemberSession,
        auth_member_repo: IVerifiableAuthentication,
    ):
        assert issubclass(
            type(pass_repo), IChangeablePasswd
        ), "auth_member_repo must be a class that inherits from  IChangeablePasswd."
        assert issubclass(
            type(load_session_repo), ILoadableSession
        ), "load_session_repo must be a class that inherits from ILoadableSession."
        assert issubclass(
            type(auth_member_repo), IVerifiableAuthentication
        ), "auth_member_repo must be a class that inherits from IverifiableAuthentication."

        self.pass_repo = pass_repo
        self.load_session_repo = load_session_repo
        # self.make_session_repo = make_session_repo
        self.auth_repo = auth_member_repo

    def change_expired_pw(
        self,
        user_key: str,
        old_passwd: str,
        new_passwd: str,
    ) -> Result[MemberID, str]:
        
        builder = MemberSessionBuilder().set_deserialize_key(user_key)
        match self.load_session_repo.load_session(user_key):
            case Ok(json):
                match builder.set_deserialize_value(json):
                    case Ok(session):
                        user_session = session.build()
                        member_id = user_session.member_id
                        account = user_session.account                        
                    case _:
                        return Err("Invalid Member Session")
            case _:
                return Err("plz login")
        
        match self.auth_repo.identify_and_authenticate(account, hashing_passwd(old_passwd)):
            case Ok(_):
                return self.pass_repo.update_passwd(member_id, hashing_passwd(new_passwd))
            case _:
                return Err("Incorrect password")
