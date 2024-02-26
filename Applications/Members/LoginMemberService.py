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


class AuthenticationMemberService:
    def __init__(
        self,
        auth_member_repo: IVerifiableAuthentication,
        session_repo: IMakeSaveMemberSession,
    ):
        assert issubclass(
            type(auth_member_repo), IVerifiableAuthentication
        ), "auth_member_repo must be a class that inherits from IverifiableAuthentication."

        self.auth_repo = auth_member_repo
        self.session_repo = session_repo

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
        login_result = self.auth_repo.identify_and_authenticate(
            account, hashing_passwd(passwd)
        )

        match login_result:
            case Ok(auth):
                ic()
                time = self.get_block_time(auth.fail_count)
                time = self.get_block_time(auth.fail_count)
                if not self.check_login_able(auth.last_access, time):
                    return Err(f"block : {time}")
                ret = auth

            case Err(e):
                return Err("아이디가 존재하지 않습니다. 회원가입을 해주세요.")

        if ret.is_sucess:
            session_result = self.session_repo.make_and_save_session(ret.id)
            match session_result:
                case Ok(session):
                    # MemberSession 생성
                    # member_session = MemberSessionBuilder().set_deserialize_key(ret.id.get_id()).set_deserialize_value(session).build()
                    return Ok(session)
                case Err(_):
                    return session_result
                case _:
                    assert False, "Value Error"
        else:
            self.auth_repo.update_access(ret)
            ic(login_result)
            return Err("비밀번호가 틀렸습니다.")

    def get_block_time(self, num_of_incorrect_login: int) -> int:
        """_summary_
        틀린 횟수에 따른 정지시간을 관리한다.
        Args:
            num_of_incorrect (int): _description_

        Returns:
            int: 제한 하는 분 반환 / 제한을 하지 않으면 0반환
        """
        #
        self.block_rule_list: List[Tuple[int, int]] = [
            (3, 5),  # 3회 틀리면, 5분
            (5, 30),  # 5회 틀리면 30분
            (7, 60),  # 7회 틀리면 1시간
            (9, 1440),  # 9회 틀리면 하루
            (11, 4320),  # 11회 틀리면 3일
        ]
        self.max_block: Tuple[int, int, int] = (
            13,
            2,
            10080,
        )  # 13회 이후부터는 2번 틀릴때마다 일주일씩 블락
        for threshold, block_time in self.block_rule_list:
            if num_of_incorrect_login == threshold:
                return block_time

        # 횟수가 최대 횟수를 초과하는 경우 최대 정지 시간 적용
        match num_of_incorrect_login - self.max_block[0]:
            case minus if minus < 0:  # not max
                return 0
            case up_max:
                return ((up_max + 1) % self.max_block[1]) * self.max_block[2]

    def check_login_able(self, last_access: datetime, block_minute: int) -> bool:
        """
        로그인 가능 여부를 확인하는 함수
        """
        # 잠긴 상태에서 시간이 지난 경우 잠금 해제
        if last_access < datetime.now() - timedelta(minutes=block_minute):
            return True
        else:
            return False
