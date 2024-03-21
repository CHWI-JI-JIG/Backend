import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional, Tuple, List
from result import Result, Ok, Err
from datetime import datetime, timedelta

from uuid import uuid4, UUID

from Domains.Members import *
from Domains.Products import *
from Domains.Sessions import *
from Builders.Members import *
from Builders.Products import *
from Repositories.Members import *
from Repositories.Products import *
from Repositories.Sessions import *

from icecream import ic


class AdminService:
    def __init__(
        self,
        read_repo: IReadableMemberList,
        edit_repo: IEditableMember,
    ):
        assert issubclass(
            type(read_repo), IReadableMemberList
        ), "read_repo must be a class that inherits from IReadableMemberList."
        assert issubclass(
            type(edit_repo), IEditableMember
        ), "save_member_repo must be a class that inherits from  IEditableMember."

        self.read_repo = read_repo
        self.edit_repo = edit_repo

    def read_members(
        self,
        page=0,
        size=10,
    ) -> Result[Tuple[int, List[Member]], str]:
        return self.read_repo.get_members(page=page, size=size)

    def change_role(
        self,
        role: str,
        user_id: str,
    ) -> Result[MemberID, str]:
        try:
            role_type = RoleType(role)
        except ValueError:
            return Err("Invalid role type")
        except Exception as e:
            return Err(str(e))
        match MemberIDBuilder().set_uuid(user_id).map(lambda b: b.build()):
            case Ok(member_id):
                return self.edit_repo.update_role(member_id, role_type)
            case e:
                return e
