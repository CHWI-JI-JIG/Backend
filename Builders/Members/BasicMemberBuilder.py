import __init__
from typing import Optional, Self, List, Union, Callable
from uuid import uuid4, UUID
from datetime import datetime
import pytz

from Commons.helpers import check_hex_string
from Commons.format import KOREA_TIME_FORMAT
from Domains.Members import *

from icecream import ic


class MemberIDBuilder(IMemberIDBuilder):
    def __init__(self):
        self.uuid: Optional[UUID] = None
        self.sequence: Optional[int] = None

    def set_seqence(self, seq: int) -> Self:
        assert isinstance(seq, int), "Type of seq is int."
        assert self.sequence is None, "The sequence is already set."
        assert seq >= 0, "seq >= 0"

        self.sequence = seq
        return self

    def set_uuid4(self) -> Self:
        assert self.uuid is None, "The UUID is already set."

        self.uuid = uuid4()
        return self

    def set_uuid_hex(self, uuid_hex: str) -> Self:

        assert self.uuid is None, "The UUID is already set."
        assert check_hex_string(uuid_hex), "The uuid_hex is not in hex format."

        self.uuid = UUID(hex=uuid_hex)
        return self

    def build(self) -> MemberID:
        match (self.uuid, self.sequence):
            case (uuid, seq) if isinstance(uuid, UUID):
                if seq is None:
                    seq = -1

                return MemberID(
                    uuid=uuid,
                    sequence=seq,
                )
            case (None, None):
                assert False, "You didn't set the uuid and seqence."
            case (None, seq) if isinstance(seq, int):
                assert False, "You didn't set the uuid."
            case _:
                assert False, "Unknown Error"


class NoFilterMemberBuilder(IMemberBuilder):
    def __init__(
        self,
        passwd_converter: Callable[[str], str] = (lambda x: x),
    ):
        self.id: Optional[MemberID] = None
        self.account: Optional[str] = None
        self.passwd: Optional[str] = None
        self.role: Optional[RoleType] = None

        assert isinstance(
            passwd_converter, Callable
        ), "Type of pw_converter is Callable(str)->str."
        assert isinstance(
            passwd_converter("aaa"), str
        ), "Type of pw_converter is Callable(str)->str."
        self.pw_converter = passwd_converter

    def set_id(self, id: Optional[MemberID] = None) -> Self:
        assert self.id is None, "id is already set."

        if id is None:
            id = MemberIDBuilder().set_uuid4().build()

        assert isinstance(
            id, MemberID
        ), "ValueType Error: Initialize the id via MemberIDBuilder."

        self.id = id
        return self

    def set_account(self, account: str) -> Self:
        assert self.account is None, "account is already set."
        assert isinstance(account, str), "Type of account is str"

        self.account = account
        return self

    def set_passwd(self, passwd: str) -> Self:
        assert self.passwd is None, "passwd is already set."
        assert isinstance(passwd, str), "Type of account is str"

        self.passwd = self.pw_converter(passwd)
        return self

    def set_role(self, role: str) -> Self:
        assert self.role is None, "rule is already set."
        assert isinstance(role, str), "Type of rule is str."

        self.role = RoleType[role.strip(" \n\t").upper()]
        assert self.role.name in list(
            RoleType._member_names_
        ), "Type of rule is RuleType. "

        return self

    def build(self) -> Member:
        assert isinstance(self.id, MemberID), "You didn't set the id."
        assert isinstance(self.account, str), "You didn't set the account."
        assert isinstance(self.role, RoleType), "You didn't set the rule."

        return Member(
            id=self.id,
            account=self.account,
            passwd=self.passwd,
            role=self.role,
        )


class NoFilterPrivacyBuilder(IPrivacyBuilder):
    def __init__(
        self,
        name: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        address: Optional[str] = None,
        pay_account: Optional[str] = None,
        company_registration_number: Optional[str] = None,
    ):
        self.id: Optional[MemberID] = None
        self.name: Optional[str] = name
        self.phone: Optional[str] = phone
        self.email: Optional[str] = email
        self.address: Optional[str] = address
        self.pay_account: Optional[str] = pay_account
        self.company_registration_number: Optional[str] = company_registration_number

    def set_id(self, id: MemberID) -> Self:
        assert self.id is None, "id is already set."

        if id is None:
            id = MemberIDBuilder().set_uuid4().build()

        assert isinstance(
            id, MemberID
        ), "ValueType Error: Initialize the id via MemberIDBuilder.set_uuid_hex(str) and put it in."

        self.id = id
        return self

    def set_name(self, name: str) -> Self:
        assert self.name is None, "name is already set."
        assert isinstance(name, str), "Type of name is str"

        self.name = name
        return self

    def set_phone(self, phone: str) -> Self:
        assert self.phone is None, "phone is already set."
        assert isinstance(phone, str), "Type of phone is str"

        self.phone = phone
        return self

    def set_email(self, email: str) -> Self:
        assert self.email is None, "email is already set."
        assert isinstance(email, str), "Type of email is str"

        self.email = email
        return self

    def set_address(self, address: str) -> Self:
        assert self.address is None, "address is already set."
        assert isinstance(address, str), "Type of address is str"

        self.address = address
        return self

    def set_company_registration_number(self, company_registration_number: str) -> Self:
        assert (
            self.company_registration_number is None
        ), "company_registration_number is already set."
        assert isinstance(
            company_registration_number, str
        ), "Type of company_registration_number is str"

        self.company_registration_number = company_registration_number
        return self

    def set_pay_account(self, pay_account: str) -> Self:
        assert self.pay_account is None, "pay_account is already set."
        assert isinstance(pay_account, str), "Type of pay_account is str"

        self.pay_account = pay_account
        return self

    def build(self) -> Privacy:
        assert isinstance(self.id, MemberID), "You didn't set the id."
        assert isinstance(self.name, str), "You didn't set the name."
        assert isinstance(self.phone, str), "You didn't set the phone."
        assert isinstance(self.email, str), "You didn't set the email."
        assert isinstance(self.address, str), "You didn't set the address."

        return Privacy(
            id=self.id,
            name=self.name,
            phone=self.phone,
            email=self.email,
            address=self.address,
            pay_account=self.pay_account,
            company_registration_number=self.company_registration_number,
        )


class AuthenticationBuilder(IAuthenticationBuilder):
    def __init__(
        self,
        cnt: Optional[int] = None,
    ):
        self.id: Optional[MemberID] = None
        self.fail_count: Optional[int] = cnt
        self.last_access: Optional[datetime] = None
        self.is_sucess: Optional[bool] = None

    def set_id(self, id: Optional[MemberID] = None) -> Self:
        assert self.id is None, "id is already set."

        if id is None:
            id = MemberIDBuilder().set_uuid4().build()

        assert isinstance(
            id, MemberID
        ), "ValueType Error: Initialize the id via MemberIDBuilder.set_uuid_hex(str) and put it in."

        self.id = id
        return self

    def set_fail_count(self, count: int) -> Self:
        assert self.fail_count is None, "fail count is already set."
        assert count >= 0, "count >= 0"

        self.fail_count = count
        return self

    def set_is_sucess(self, is_sucess: bool) -> Self:
        assert self.is_sucess is None, "fail count is already set."
        assert isinstance(is_sucess, bool), "is_sucess is bool."

        self.is_sucess = is_sucess
        return self

    def set_last_access(self, time: Optional[datetime] = None) -> Self:
        assert self.last_access is None, "time is already set."

        if time is None:
            self.last_access = datetime.now()
            return self

        assert isinstance(time, datetime), "Type of time is datetime."

        self.last_access = time
        return self

    def build(self) -> Authentication:
        assert isinstance(self.id, MemberID), "You didn't set the id."
        assert isinstance(self.fail_count, int), "You didn't set the fail_count."
        assert isinstance(self.last_access, datetime), "You didn't set the last_access."
        assert isinstance(self.is_sucess, bool), "You didn't set the is_sucess."

        return Authentication(
            id=self.id,
            last_access=self.last_access,
            fail_count=self.fail_count,
            is_sucess=self.is_sucess,
        )


class PayDataBuilder(IPayDataBuilder):
    def __init__(
        self,
    ):
        self.id: Optional[MemberID] = None
        self.pay_account_list: List[str] = []

    def set_id(self, id: Optional[MemberID] = None) -> Self:
        assert self.id is None, "id is already set."

        if id is None:
            id = MemberIDBuilder().set_uuid4().build()

        assert isinstance(
            id, MemberID
        ), "ValueType Error: Initialize the id via MemberIDBuilder.set_uuid_hex(str) and put it in."

        self.id = id
        return self

    def add_pay_account(self, pay_account: Union[List[str], str]) -> Self:
        match pay_account:
            case str_pay if isinstance(str_pay, str):
                self.pay_account_list.append(str_pay)
            case list_pay if isinstance(list_pay, list):
                for pay in list_pay:
                    assert isinstance(pay, str), "Type of pay is str."
                    self.pay_account_list.append(pay)
            case _:
                assert False, "Type of pay is str."

        return self

    def build(self) -> PayData:
        assert isinstance(self.id, MemberID), "You didn't set the id."
        assert len(self.pay_account_list) > 0, "You didn't set the pay_account."

        return PayData(
            id=self.id,
            pay_account_list=self.pay_account_list,
        )
