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
from Repositories.Sessions import IMakeSaveMemberSession, ILoadableSession,IDeleteableSession

from icecream import ic


class AuthenticationMemberService:
    def __init__(
        self,
        auth_member_repo: IVerifiableAuthentication,
        session_repo: IMakeSaveMemberSession,
        load_repo : ILoadableSession,
        del_session_repo : IDeleteableSession,
    ):
        assert issubclass(
            type(auth_member_repo), IVerifiableAuthentication
        ), "auth_member_repo must be a class that inherits from IverifiableAuthentication."

        self.auth_repo = auth_member_repo
        self.session_repo = session_repo
        self.load_repo = load_repo
        self.del_session_repo = del_session_repo

    def login(self, account: str, passwd: str) -> Result[Tuple[MemberSession,bool], str]:
        """_summary_

        Args:
            account (str): _description_
            passwd (str): _description_

        Returns:
            Result[Tuple[MemberSession,bool], str]:
                Ok(Tuple[MemberSession,bool]):
                    bool: 비밀번호 변경 필요 여부 | 변경 필요 시 true
                Err(str):
        """

        match self.auth_repo.identify_and_authenticate(account, hashing_passwd(passwd)):
            case Ok(auth):
                block_time = self.get_block_time(auth.fail_count)
                if block_time > 0 and not self.check_login_able(
                    auth.last_access, block_time
                ):
                    ic()
                    ic(block_time, auth.last_access)
                    return Err(f"block : {block_time}")
                ret = auth

            case Err(e):
                return Err("아이디가 존재하지 않습니다. 회원가입을 해주세요.")

        if ret.is_sucess:
            # 여기에 작성!!!!
            # 같은 member_id 있는지 찾아서 있다면 다 로그아웃
            id = ret.id.get_id()
            load_result = self.load_repo.load_session_from_owner_id(id)
            if load_result.is_ok():
                sessions = load_result.unwrap()  # 세션 목록을 가져옴
                for session in sessions:
                    key = session.key  # 세션 키를 가져옴
                    self.del_session_repo.delete_session_to_key(key)
                    self.del_session_repo.delete_session_to_owner_id(key)
                
            
            session_result = self.session_repo.make_and_save_session(ret.id)
            match session_result:
                case Ok(session):
                    need_password_change = self.check_passwd_change(ret.last_changed_date, session.role)
                    result = (session, need_password_change)
                    return Ok(result)
                case Err(_):
                    return session_result
                case _:
                    assert False, "Value Error"
        else:
            self.auth_repo.update_access(ret)
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
    
    def check_passwd_change(self, last_changed_date: datetime, role: str) -> bool:
        """
        비밀번호 변경이 필요한지 확인하는 함수
        """
        try:
            role_type = RoleType(role)
        except ValueError:
            return Err("Invalid role type")
        except Exception as e:
            return Err(str(e))
        
        current_date = datetime.now()
        if role_type == RoleType.ADMIN:
            days_to_check = 180  # 180 = 6 months(반기)
        else:
            days_to_check = 60  # 60 days
        days_since_last_change = (current_date - last_changed_date).days
        return days_since_last_change > days_to_check
        
        # time_since_last_change = current_date - last_changed_date
        # return time_since_last_change.total_seconds() > days_to_check
