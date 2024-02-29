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
        load_session: ILoadableSession,
    ):
        assert issubclass(
            type(read_repo), IReadableMemberList
        ), "read_repo must be a class that inherits from IReadableMemberList."
        assert issubclass(
            type(edit_repo), IEditableMember
        ), "save_member_repo must be a class that inherits from  IEditableMember."
        assert issubclass(
            type(load_session), ILoadableSession
        ), "save_member_repo must be a class that inherits from ILoadableSession."

        self.read_repo = edit_repo
        self.edit_repo = edit_repo
        self.load_session_repo = load_session

    def read_members(
        self,
        page=0,
        size=10,
    ) -> Result[Tuple[int, List[Member]], str]: ...

    def change_role(
        self,
        role: str,
        user_id: str,
    ) -> Result[MemberID, str]: ...
