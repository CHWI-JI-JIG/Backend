import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional
from result import Result, Ok, Err

from Domains.Members import *
from Builders.Members import *
from Repositories.Members import *
from Applications.Members.ExtentionMethod import hashing_passwd

from icecream import ic


class CreateProductService:
    def __init__(
        self,
        # read_member_repo: IReadableMember,
        save_member_repo: ISaveableMember,
    ):
        # self.read_repo = read_member_repo
        assert issubclass(
            type(save_member_repo), ISaveableMember
        ), "save_member_repo must be a class that inherits from ISaveableMember."

        self.save_repo = save_member_repo

    # def publish_temp_product_id(self, member_session_key:str)->

    def create(
        self,
        account: str,
        passwd: str,
        role: str,
        name: str,
        phone: str,
        email: str,
        address: str,
        company_registration_number: Optional[str] = None,
        pay_account: Optional[str] = None,
    ) -> Result[MemberID, str]:
        """_summary_

        Assert:


        Returns:
            Optional[Err]:
                Ok :Sucess
                Err : Reason for failure
                    "AccountAlreadyExists: Fail_CreateMemberService_AccountAlreadyExists"
                    "NotSameRole: There is no such thing as a {role} role."
                    "NoHaveRegistration: If User is Seller, Then Paramater need Company registration number."
                    "HavePayAccount: If User is Buyer, Then Paramater don't need Pay Account."
                    "HavePayAccount: If User is Buyer, Then Paramater don't need Pay Account."

        """

        member_builder = NoFilterMemberBuilder(passwd_converter=hashing_passwd)
        privacy_builder = NoFilterPrivacyBuilder(
            name=name,
            phone=phone,
            email=email,
            address=address,
        )
        member_builder.set_account(account=account).set_passwd(passwd)

        match role:
            case "seller":
                if not isinstance(company_registration_number, str):
                    return Err(
                        "NoHaveRegistration: If User is Seller, Then Paramater need Company registration number."
                    )
                if not isinstance(pay_account, str):
                    return Err(
                        "NoHavePayAccount: If User is Seller, Then Paramater need Pay Account."
                    )
                member_builder.set_role(role)
                privacy_builder.set_pay_account(
                    pay_account
                ).set_company_registration_number(company_registration_number)
            case "buyer":
                if company_registration_number is not None:
                    return Err(
                        "HaveRegistration: If User is Buyer, Then Paramater don't need Company registration number."
                    )
                if pay_account is not None:
                    return Err(
                        "HavePayAccount: If User is Buyer, Then Paramater don't need Pay Account."
                    )
                member_builder.set_role(role)
            case "admin":
                assert False, "NotImplementError: admin"
                if company_registration_number is not None:
                    return Err(
                        "NoHaveRegistration: If User is Seller, Then Paramater need Company registration number."
                    )
                if pay_account is not None:
                    return Err(
                        "NoHavePayAccount: If User is Seller, Then Paramater need Pay Account."
                    )
                member_builder.set_role(role)
            case _:
                return Err(f"NotSameRole: There is no such thing as a {role} role.")
        id = MemberIDBuilder().set_uuid().build()
        return self.save_repo.save_member(
            member=member_builder.set_id(id).build(),
            privacy=privacy_builder.set_id(id).build(),
        )
