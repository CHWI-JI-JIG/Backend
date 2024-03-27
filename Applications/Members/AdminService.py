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

from Applications.Sessions.SessionHelper import check_valide_session
from icecream import ic


class AdminService:
    def __init__(
        self,
        read_repo: IReadableMemberList,
        edit_repo: IEditableMember,
        load_session_repo: ILoadableSession,
    ):
        assert issubclass(
            type(read_repo), IReadableMemberList
        ), "read_repo must be a class that inherits from IReadableMemberList."
        assert issubclass(
            type(edit_repo), IEditableMember
        ), "save_member_repo must be a class that inherits from  IEditableMember."
        assert issubclass(
            type(load_session_repo), ILoadableSession
        ), "load_session_repo must be a class that inherits from ILoadableSession."
        
        self.read_repo = read_repo
        self.edit_repo = edit_repo
        self.session_repo = load_session_repo

    def read_members(
        self,
        admin_key: str,
        page=0,
        size=10,
    ) -> Result[Tuple[int, List[Member]], str]:

        builder = MemberSessionBuilder().set_deserialize_key(admin_key)
        match self.session_repo.load_session(admin_key):
            case Ok(json):
                match builder.set_deserialize_value(json).map(lambda b: b.build()):
                    case Ok(session):
                        ic(session)
                        admin_session = session
                        if admin_session.role != RoleType.ADMIN:
                            return Err("Access Denied: User is not admin")
                    case _:
                        return Err("err")

            case e:
                ic(e)
                return Err("Session load or build failed")
        return self.read_repo.get_members(page=page, size=size)

    def change_role(
        self,
        admin_key: str,
        role: str,
        target_user_id: str,
    ) -> Result[MemberID, str]:

        builder = MemberSessionBuilder().set_deserialize_key(admin_key)
        match self.session_repo.load_session(admin_key):
            case Ok(json):
                match builder.set_deserialize_value(json):
                    case Ok(session):
                        admin_session = session.build()
                        if not check_valide_session(admin_session):
                            return Err("Expired Session")
                        if admin_session.role != RoleType.ADMIN:
                            return Err("Permission denied")
                    case _:
                        return Err("Invalid Member Session")
            case _:
                return Err("Session load failed")

        try:
            role_type = RoleType(role)
        except ValueError:
            return Err("Invalid role type")
        except Exception as e:
            return Err(str(e))
        match MemberIDBuilder().set_uuid(target_user_id).map(lambda b: b.build()):
            case Ok(member_id):
                return self.edit_repo.update_role(member_id, role_type)
            case e:
                return e
