import __init__
from typing import Optional, Self
from uuid import uuid4, UUID

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

        assert isinstance(id, MemberUUID), "ValueType Error"

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
        assert isinstance(self.passwd, str), "You didn't set the passwd."
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

        assert isinstance(id, MemberUUID), "ValueType Error"

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


class AuthenticationBuilder(IMemberBuilder):
    def __init__(
        self,
    ):
        self.id: Optional[MemberID] = None
        self.rule: Optional[RuleType] = None

    def set_id(self, id: Optional[MemberID] = None) -> Self:
        assert self.id is None, "id is already set."

        if id is None:
            id = MemberIDBuilder().set_uuid4().build()

        assert isinstance(id, MemberUUID), "ValueType Error"

        self.id = id
        return self

    def build(self) -> Member:
        assert isinstance(self.id, MemberUUID), "You didn't set the id."

        return Authentication(
            id=self.id,
        )
