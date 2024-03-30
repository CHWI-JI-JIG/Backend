import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional, Tuple, List
from result import Result, Ok, Err

from uuid import uuid4, UUID

from Domains.Members import *
from Domains.Sessions import *
from Builders.Members import *
from Repositories.Members import *
from Applications.Members.ExtentionMethod import *
from datetime import datetime, timedelta
from Repositories.Sessions import *
from Applications.Sessions.SessionHelper import check_valide_session

from icecream import ic


class LoginAdminService:
    def __init__(
        self,
        auth_member_repo: IVerifiableAuthentication,
        session_repo: IMakeSaveMemberSession,
        load_repo: ILoadableSession,
        del_session_repo: IDeleteableSession,
        otp_session_repo: IMakeSaveMemberSession,
        otp_load_session_repo: ILoadableSession,
    ):
        assert issubclass(
            type(auth_member_repo), IVerifiableAuthentication
        ), "auth_member_repo must be a class that inherits from IverifiableAuthentication."
        assert issubclass(
            type(session_repo), IMakeSaveMemberSession
        ), "session_repo must be a class that inherits from IverifiableAuthentication."
        assert issubclass(
            type(load_repo), ILoadableSession
        ), "load_repo must be a class that inherits from IverifiableAuthentication."
        assert issubclass(
            type(del_session_repo), IDeleteableSession
        ), "del_session_repo must be a class that inherits from IverifiableAuthentication."
        assert issubclass(
            type(otp_session_repo), IMakeSaveMemberSession
        ), "otp_session_repo must be a class that inherits from IverifiableAuthentication."
        assert issubclass(
            type(otp_load_session_repo), ILoadableSession
        ), "otp_load_session_repo must be a class that inherits from IverifiableAuthentication."

        self.auth_repo = auth_member_repo
        self.session_repo = session_repo
        self.load_repo = load_repo
        self.del_session_repo = del_session_repo
        self.otp_session_repo = otp_session_repo
        self.otp_load_session_repo = otp_load_session_repo

    def login(self, account: str, passwd: str) -> Result[MemberSession, str]:
        """_summary_

        Args:
            account (str): _description_
            passwd (str): _description_

        Returns:
            Result[MemberSession,str]:
                Ok():
                Err(str):

        """

        match self.auth_repo.identify_and_authenticate(account, hashing_passwd(passwd)):
            case Ok(auth):
                if auth.role != RoleType.ADMIN:
                    return Err("관리자 외에 로그인할 수 없는 페이지 입니다.")

                block_time = get_block_time(auth.fail_count)
                if block_time > 0 and not check_login_able(
                    auth.last_access, block_time
                ):
                    ic()
                    ic(block_time, auth.last_access)
                    return Err(f"block : {block_time}")
                if auth.role != RoleType.ADMIN:
                    return Err("Permission Deny")
                ret = auth

            case Err(e):
                return Err("아이디가 존재하지 않습니다. 회원가입을 해주세요.")

        if ret.is_sucess:
            # access OTP repo
            session_result = self.otp_session_repo.make_and_save_session(ret.id)
            match session_result:
                case Ok(session):
                    return Ok(session)
                case Err(_):
                    return session_result
                case _:
                    assert False, "Value Error"
        else:
            self.auth_repo.update_access(ret)
            return Err("비밀번호가 틀렸습니다.")

    def otp_login(self, temp_session: str) -> Result[MemberSession, str]:
        builder = MemberSessionBuilder().set_deserialize_key(temp_session)
        # access OTP repo
        match self.otp_load_session_repo.load_session(temp_session):
            case Ok(json):
                match builder.set_deserialize_value(json):
                    case Ok(session):
                        user_session = session.build()
                        if not check_valide_session(user_session):
                            return Err("Expired Session")
                        if user_session.role != RoleType.ADMIN:
                            return Err("Permission Deny")
                    case _:
                        return Err("Invalid Member Session")
            case e:
                ic(e)
                return Err("plz login")

        # 같은 member_id 있는지 찾아서 있다면 다 로그아웃
        id = user_session.member_id.get_id()
        match self.load_repo.load_session_from_owner_id(id):
            case Ok(tokens):
                for session in tokens:
                    key = session.key  # 세션 키를 가져옴
                    self.del_session_repo.delete_session_to_key(key)
                    self.del_session_repo.delete_session_to_owner_id(key)
            case e:
                return e

        match self.session_repo.make_and_save_session(user_session.member_id):
            case Ok(session):
                return Ok(session)
            case e:
                ic(e)
                return e