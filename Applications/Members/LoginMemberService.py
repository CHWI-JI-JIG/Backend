import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional, Tuple, List
from result import Result, Ok, Err

from Domains.Members import *
from Builders.Members import *
from Repositories.Members import *
from Applications.Members.ExtentionMethod import hashing_passwd

from icecream import ic


class AuthenticationMemberService:
    def __init__(
        self,
        auth_member_repo: IVerifiableAuthentication,
    ):
        assert issubclass(
            type(auth_member_repo), IVerifiableAuthentication
        ), "auth_member_repo must be a class that inherits from IverifiableAuthentication."

        self.auto_repo = auth_member_repo
    def login(self, account:str, passwd:str) -> Result[,str]:
        ...

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