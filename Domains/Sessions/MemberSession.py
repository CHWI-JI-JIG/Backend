import __init__
from dataclasses import dataclass
from abc import ABCMeta, abstractmethod
from typing import Optional, Self
from uuid import uuid4, UUID
import json


from Commons.helpers import check_hex_string
from Domains.Sessions import ISessionSerializeable, ISesseionBuilder
from Domains import ID
from Domains.Members import *
from Builders.Members import *

from icecream import ic


@dataclass(frozen=True)
class MemberSession(ISessionSerializeable, ID):
    key: UUID
    name: str
    role: RoleType
    member_id: MemberID
    seq: int = -1

    def get_id(self) -> str:
        return self.key.hex

    def serialize_key(self) -> str:
        return self.get_id()

    def serialize_value(self) -> str:
        return json.dumps(
            {
                "seq": str(self.seq),
                "member_id": self.member_id.get_id(),
                "name": self.name,
                "role": str(self.role),
            },
            ensure_ascii=False,
        )


class MemberSessionBuilder(ISesseionBuilder):
    def __init__(
        self,
        key: Optional[UUID] = None,
        member_id: Optional[MemberID] = None,
        name: Optional[str] = None,
        seq: int = -1,
    ):
        self.seq = seq
        self.key = key
        self.mid = member_id
        self.name: Optional[str] = name
        self.role: Optional[RoleType] = None

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

        dict_key = "member_id"
        assert isinstance(to_dict.get(dict_key), str), f"{dict_key} is not exsist dict."
        self.set_member_id(to_dict.get(dict_key))

        dict_key = "seq"
        assert isinstance(to_dict.get(dict_key), str), f"{dict_key} is not exsist dict."
        self.set_seqence(int(to_dict.get(dict_key)))

        dict_key = "name"
        assert isinstance(to_dict.get(dict_key), str), f"{dict_key} is not exsist dict."
        self.set_name(to_dict.get(dict_key))

        dict_key = "role"
        assert isinstance(to_dict.get(dict_key), str), f"{dict_key} is not exsist dict."
        self.set_role(to_dict.get(dict_key))

        return self

    def set_name(self, name: str) -> Self:
        assert self.name is None, "name is already set."
        assert isinstance(name, str), "Type of name is str"

        self.name = name
        return self

    def set_role(self, role: str) -> Self:
        assert self.role is None, "rule is already set."
        assert isinstance(role, str), "Type of rule is str."

        self.role = RoleType[role.strip(" \n\t").upper()]
        assert self.role.name in list(
            RoleType._member_names_
        ), "Type of rule is RuleType. "

        return self

    def set_seqence(self, seq: int) -> Self:
        assert isinstance(seq, int), "Type of seq is int."
        assert self.seq < 0, "The sequence is already set."
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
            case _:
                assert False, "Type of key is str."

        return self

    def set_member_id(self, member_id: Optional[str] = None) -> Self:
        assert self.mid is None, "member id is already set."

        if member_id is None:
            id = MemberIDBuilder().set_uuid().build()
        elif isinstance(member_id, str):
            id = MemberIDBuilder().set_uuid(member_id).build()
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
        assert isinstance(self.role, RoleType), "You didn't set the rule."
        assert isinstance(self.name, str), "You didn't set the name."

        return MemberSession(
            seq=self.seq,
            key=self.key,
            member_id=self.mid,
            role=self.role,
            name=self.name,
        )
