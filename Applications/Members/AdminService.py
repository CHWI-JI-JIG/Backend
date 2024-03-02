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
        ), "save_member_repo must be a class that inherits from ILoadableSession."

        self.read_repo = read_repo
        self.edit_repo = edit_repo
        self.load_session_repo = load_session_repo

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
        #load_result = self.read_repo.get_members(user_id)
        #ic()
        #match load_result:
        #    case Ok(member):
        #        new_role = "seller" if role == "buyer" else "buyer"
        #        role = new_role
        #        update_result = self.edit_repo.update_member(member)
        #        ic( )
        #        match update_result:
        #            case Ok(member_id):
        #                ic()
        #                Ok(member_id)
        #            case Err(err_msg):
        #                ic()
        #                Err(err_msg)
        #    case Err(err_msg):
        #        ic()
        #        Err(err_msg)
                
                
        load_result = self.read_repo.get_members(user_id)
        ic()
        match load_result:
            case Ok(member):
                new_role = "seller" if role == "buyer" else "buyer"
                role = new_role
                update_result = self.edit_repo.update_member(member)
                ic( )
                match update_result:
                    case Ok(member_id):
                        ic()
                        Ok(member_id)
                    case Err(err_msg):
                        ic()
                        Err(err_msg)
            case Err(err_msg):
                ic()
                Err(err_msg)
