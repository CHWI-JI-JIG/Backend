import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional
from result import Result, Ok, Err

from Domains.Members import *
from Builders.Members import *
from Repositories.Members import *


class CreateMemberService:
    def __init__(
        self,
        read_member_repo: IReadableMember,
        save_member_repo: ISaveableMember,
    ):
        self.read_repo = read_member_repo
        self.save_repo = save_member_repo

    def create(
        self,
        account: str,
        passwd: str,
        rule: str,
        name: str,
        phone: str,
        email: str,
        company_registration_number: Optional[str],
    ) -> Result[Optional[str], str]:
        """_summary_

        Returns:
            Optional[Err]:
                Ok :
                    None : Sucess
                    str : Reason for failure
                Err : Err
        """
        member_builder = NoFilterMemberBuilder()

        if self.read_repo.check_exist_account(account=account):
            return Ok("Fail_CreateMemberService_AccountAlreadyExists")
        member_builder.set_account(account=account).set_passwd()
