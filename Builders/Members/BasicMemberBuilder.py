import __init__
from typing import Optional, Self
from uuid import uuid4, UUID
from datetime import datetime
import pytz

from Commons.format import KOREA_TIME_FORMAT
from Domains.Members import *


class MemberIDBuilder(IMemberIDBuilder):
    def __init__(self):
        self.uuid: Optional[UUID] = None
        self.sequence: Optional[int] = None

    def set_seqence(self, seq: int) -> Self:
        assert isinstance(seq, int), "ValueError"
        assert seq >= 0, "seq >= 0"

        self.sequence = seq
        return self

    def set_uuid4(self) -> Self:
        assert self.uuid is None, "The UUID is already set."

        self.uuid = uuid4()
        return self

    def set_uuid_hex(self, uuid_hex: str) -> Self:
        from Commons.helpers import check_hex_string

        assert self.uuid is None, "The UUID is already set."
        assert check_hex_string(uuid_hex), "The uuid_hex is not in hex format."

        self.uuid = UUID(hex=uuid_hex)
        return self

    def build(self) -> MemberID:
        match (self.uuid, self.sequence):
            case (uuid, seq) if isinstance(uuid, UUID):
                if seq is None:
                    seq = -1

                return MemberUUID(
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
        account: Optional[str] = None,
        passwd: Optional[str] = None,
    ):
        self.id: Optional[MemberID] = None
        self.account: Optional[str] = account
        self.passwd: Optional[str] = passwd
        self.rule: Optional[RuleType] = None

    def set_id(self, id: Optional[MemberID] = None) -> Self:
        assert self.id is None, "id is already set."

        if id is None:
            id = MemberIDBuilder().set_uuid4().build()

        assert isinstance(
            id, MemberUUID
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
        self.passwd = passwd
        return self

    def set_rule(self, rule: str) -> Self:
        assert self.rule is None, "rule is already set."
        assert isinstance(rule, str), "Type of rule is str."

        self.rule = RuleType[rule.strip(" \n\t").upper()]
        assert isinstance(rule, RuleType), "Type of rule is RuleType. "

        return self

    def build(self) -> Member:
        assert isinstance(self.id, MemberUUID), "You didn't set the id."
        assert isinstance(self.account, str), "You didn't set the account."
        assert isinstance(self.rule, RuleType), "You didn't set the rule."

        return Member(
            id=self.id,
            account=self.account,
            passwd=self.passwd,
            rule=self.rule,
        )


class NoFilterPrivacyBuilder(IPrivacyBuilder):
    def __init__(
        self,
        name: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        address: Optional[str] = None,
        company_registration_number: Optional[str] = None,
    ):
        self.id: Optional[MemberID] = None
        self.name: Optional[str] = name
        self.phone: Optional[str] = phone
        self.email: Optional[str] = email
        self.address: Optional[str] = address
        self.company_registration_number: Optional[str] = company_registration_number

    def set_id(self, id: MemberID) -> Self:
        assert self.id is None, "id is already set."

        if id is None:
            id = MemberIDBuilder().set_uuid4().build()

        assert isinstance(
            id, MemberUUID
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

    def build(self) -> Privacy:
        assert isinstance(self.id, MemberUUID), "You didn't set the id."
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
            id, MemberUUID
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

    def set_last_access(
        self, time: Optional[str] = None, input_timezone: str = "UTC"
    ) -> Self:
        assert self.time is None, "time is already set."

        if time is None:
            self.time = datetime.now(pytz.utc)
            return self

        assert isinstance(time, str), "Type of time is str."
        assert isinstance(input_timezone, str), "Type of input_timezone is str."

        match input_timezone.lower():
            case "utc":
                convert_time = datetime.fromisoformat(time).replace(tzinfo=pytz.utc)
            case "asia/seoul" | "korea" | "korean" | "k":
                tz = pytz.timezone("Asia/Seoul")
                convert_time = tz.localize(
                    datetime.strptime(time, KOREA_TIME_FORMAT)
                ).astimezone(pytz.utc)
            case _:
                assert False, "There are only two timezones: UTC or Korea time."

        assert convert_time.utcoffset() == pytz.utc, "Not in UTC time."

        self.time = convert_time
        return self

    def build(self) -> Member:
        assert isinstance(self.id, MemberUUID), "You didn't set the id."
        assert isinstance(self.fail_count, int), "You didn't set the fail_count."
        assert isinstance(self.last_access, datetime), "You didn't set the last_access."
        assert isinstance(self.is_sucess, datetime), "You didn't set the is_sucess."

        return Authentication(
            id=self.id,
            last_access=self.last_access,
            fail_count=self.fail_count,
            is_sucess=self.is_sucess,
        )
