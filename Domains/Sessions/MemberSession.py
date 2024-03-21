import __init__
from dataclasses import dataclass
from abc import ABCMeta, abstractmethod
from typing import Optional, Self
from uuid import uuid4, UUID
from datetime import datetime
import json


from Commons.helpers import check_hex_string
from Domains.Sessions import (
    ISessionSerializeable,
    ISesseionBuilder,
    SecuritySession,
    SecuritySessionBuilder,
    SessionToken,
)
from Domains import ID
from Domains.Members import *
from Builders.Members import *
from result import Result, Ok, Err
from icecream import ic


@dataclass(frozen=True)
class MemberSession(ISessionSerializeable, ID, SecuritySession):
    name: str
    role: RoleType
    member_id: MemberID

    def get_id(self) -> str:
        return self.get_key()

    def serialize_key(self) -> str:
        return self.get_id()

    def serialize_value(self) -> str:
        return json.dumps(
            {
                "member_id": self.member_id.get_id(),
                "name": self.name,
                "role": str(self.role),
            },
            ensure_ascii=False,
        )


class MemberSessionBuilder(ISesseionBuilder, SecuritySessionBuilder):
    def __init__(
        self,
        key: Optional[UUID] = None,
        member_id: Optional[MemberID] = None,
        name: Optional[str] = None,
        owner_id: Optional[UUID] = None,
        use_count: Optional[int] = None,
        create_time: Optional[datetime] = None,
    ):
        super().__init__(
            key=key,
            owner_id=owner_id,
            use_count=use_count,
            create_time=create_time,
        )
        self.mid = member_id
        self.name: Optional[str] = name
        self.role: Optional[RoleType] = None

    def set_deserialize_key(self, key: str) -> Self:
        self.set_key(key)
        return self

    def set_deserialize_value(self, token: SessionToken) -> Result[Self, str]:
        assert isinstance(token, SessionToken), "Type of token is SessionToken."
        try:
            to_dict = json.loads(token.value)
        except:
            return Err("fali read json")
        assert isinstance(to_dict, dict), "Type of convert value is Dict."

        dict_key = "member_id"
        assert isinstance(to_dict.get(dict_key), str), f"{dict_key} is not exsist dict."
        if not isinstance(to_dict.get(dict_key), str):
            return Err(f"Not Exists {dict_key}")
        self.set_member_id(to_dict.get(dict_key))

        dict_key = "name"
        assert isinstance(to_dict.get(dict_key), str), f"{dict_key} is not exsist dict."
        if not isinstance(to_dict.get(dict_key), str):
            return Err(f"Not Exists {dict_key}")
        self.set_name(to_dict.get(dict_key))

        dict_key = "role"
        assert isinstance(to_dict.get(dict_key), str), f"{dict_key} is not exsist dict."
        if not isinstance(to_dict.get(dict_key), str):
            return Err(f"Not Exists {dict_key}")
        self.set_role(to_dict.get(dict_key))
        
        return (
            self.set_use_count(token.use_count)
            .set_create_time(token.create_time)
            .set_owner_id(token.owner_id)
        )


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

    def set_member_id(self, member_id: Optional[str] = None) -> Result[Self, str]:
        assert self.mid is None, "member id is already set."

        if member_id is None:
            id = MemberIDBuilder().set_uuid().map(lambda b: b.build())
        elif isinstance(member_id, str):
            id = MemberIDBuilder().set_uuid(member_id).map(lambda b: b.build())
        else:
            assert False, "Type of member_id is str."

        match id:
            case Ok(id):
                id = id
            case e:
                return e

        assert isinstance(
            id, MemberID
        ), "ValueType Error: Initialize the id via MemberIDBuilder."

        self.mid = id
        return Ok(self)

    def build(self) -> MemberSession:
        assert isinstance(self.mid, MemberID), "You didn't set the member_id."
        assert isinstance(self.role, RoleType), "You didn't set the rule."
        assert isinstance(self.name, str), "You didn't set the name."
        self.assert_and_check_about_setting()

        return MemberSession(
            key=self.key,
            owner_id=self.owner_id,
            name=self.name,
            role=self.role,
            member_id=self.mid,
            create_time=self.create_time,
            use_count=self.use_count,
        )
