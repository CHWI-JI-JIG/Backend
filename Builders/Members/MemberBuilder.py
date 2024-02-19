import __init__
from typing import Optional, Self
from uuid import uuid4, UUID

from Domains.Members import (
    IMemberBuilder,
    IMemberIDBuilder,
    Member,
    MemberUUID,
    MemberID,
)


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


class NoFillterMemberBuilder(IMemberBuilder):
    def __init__(
        self,
        id: Optional[str] = None,
        passwd: Optional[str] = None,
    ):
        self.id: Optional[MemberID] = None
        self.account: Optional[str] = id
        self.passwd: Optional[str] = passwd

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

    def build(self) -> Member:
        assert isinstance(self.id, MemberUUID), "You didn't set the id."
        assert isinstance(self.account, str), "You didn't set the account."
        assert isinstance(self.passwd, str), "You didn't set the passwd."

        return Member(
            id=self.id,
            account=self.account,
            passwd=self.passwd,
        )
