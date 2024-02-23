import __init__
from dataclasses import dataclass
from abc import ABCMeta, abstractmethod
from typing import Optional, Self
from uuid import uuid4, UUID
import json


from Commons.helpers import check_hex_string
from Domains.Sessions import ISesseionSerializeable, ISesseionBuilder
from Domains import ID
from Domains.Members import MemberID
from Builders.Members import *

from icecream import ic


@dataclass(frozen=True)
class MemberSession(ISesseionSerializeable, ID):
    seq: Optional[int]
    key: UUID
    member_id: MemberID

    def get_id(self) -> str:
        return self.key.hex

    def serialize_key(self) -> str:
        return self.get_id()

    def serialize_value(self) -> str:
        return json.dumps(
            {
                "member_id": self.member_id.get_id(),
            }
        )


class MemberSessionBuilder(ISesseionBuilder):
    def __init__(
        self,
        key: Optional[UUID] = None,
        member_id: Optional[MemberID] = None,
        seq: Optional[int] = None,
    ):
        self.seq = seq
        self.key = key
        self.mid = member_id

    def set_deserialize_key(self, key: str) -> Self:
        self.set_key(key)
        return self

    def set_deserialize_value(self, value: str) -> Self:
        assert isinstance(value, str), "Type of value is str."
        try:
            to_dict = json.loads(value)
        except:
            assert False, "The value is not converted to JSON."
        assert isinstance(to_dict, dict), "Type of convert value is Dict."
        assert isinstance(
            to_dict.get("member_id"), str
        ), "member_id is not exsist dict."
        self.set_member_id(to_dict.get("member_id"))
        return self

    def set_seqence(self, seq: int) -> Self:
        assert isinstance(seq, int), "Type of seq is int."
        assert self.sequence is None, "The sequence is already set."
        assert seq >= 0, "seq >= 0"

        self.seq = seq
        return self

    def set_key(self, key: Optional[str] = None) -> Self:
        assert self.key is None, "The Key is already set."
        match key:
            case None:
                self.key = uuid4()
            case k if isinstance(key, str):
                assert check_hex_string(k), "The uuid_hex is not in hex format."
                self.key = UUID(hex=key)

        return self

    def set_member_id(self, member_id: Optional[str] = None) -> Self:
        assert self.mid is None, "member id is already set."

        if member_id is None:
            id = MemberIDBuilder().set_uuid4().build()
        elif isinstance(member_id, str):
            id = MemberIDBuilder().set_uuid_hex(member_id).build()
        else:
            assert False, "Type of member_id is str."

        assert isinstance(
            id, MemberID
        ), "ValueType Error: Initialize the id via MemberIDBuilder."

        self.mid = id
        return self

    def build(self) -> MemberSession:
        assert isinstance(self.mid, MemberID), "You didn't set the member_id."
        assert isinstance(self.key, UUID), "You didn't set the key."

        return MemberSession(
            seq=self.seq,
            key=self.key,
            member_id=self.mid,
        )
