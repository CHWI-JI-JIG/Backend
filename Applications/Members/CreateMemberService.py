import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional
from result import Result, Ok, Err

from Domains.Members import *
from Builders.Members import *
from Repositories.Members import *
from Applications.Members.ExtentionMethod import hashing_passwd


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
        role: str,
        name: str,
        phone: str,
        email: str,
        company_registration_number: Optional[str] = None,
        pay_account: Optional[str] = None,
    ) -> Result[Optional[str], str]:
        """_summary_

        Returns:
            Optional[Err]:
                Ok :Sucess
                Err : Reason for failure
                    "AccountAlreadyExists: Fail_CreateMemberService_AccountAlreadyExists"
                    "NotSameRole: There is no such thing as a {role} role."
        """
        member_builder = NoFilterMemberBuilder(passwd_converter=hashing_passwd)
        privacy_builder = NoFilterPrivacyBuilder(
            name=name,
            phone=phone,
            email=email,
        )

        if self.read_repo.check_exist_account(account=account):
            return Err(
                "AccountAlreadyExists: Fail_CreateMemberService_AccountAlreadyExists"
            )
        member_builder.set_account(account=account).set_passwd(passwd)

        match role:
            case "seller":
                if not isinstance(company_registration_number, str):
                    return Err("")
                member_builder.set_role(role)
                privacy_builder.set_company_registration_number(
                    company_registration_number
                )
            case "buyer":
                member_builder.set_role(role)
            case "abmin":
                member_builder.set_account(role)
            case _:
                return Err(f"NotSameRole: There is no such thing as a {role} role.")
