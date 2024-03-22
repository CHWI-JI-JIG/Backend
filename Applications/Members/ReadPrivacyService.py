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


class ReadPrivacyService:
    def __init__(
        self,
        read_repo: IReadableMember,
        load_session_repo: ILoadableSession,
    ):
        assert issubclass(
            type(read_repo), IReadableMember
        ), "read_repo must be a class that inherits from IReadableMember."
        assert issubclass(
            type(load_session_repo), ILoadableSession
        ), "save_member_repo must be a class that inherits from ILoadableSession."

        self.read_repo = read_repo
        self.load_session_repo = load_session_repo

    def read_privacy(self, user_session_key: str) -> Result[Privacy, str]:

        builder = MemberSessionBuilder().set_deserialize_key(user_session_key)

        match self.load_session_repo.load_session(user_session_key):
            case Ok(json):
                match builder.set_deserialize_value(json).map(lambda b: b.build()):
                    case Ok(session):
                        seller_id = session.member_id
                    case _:
                        return Err("Invalid Member Session")
            case e:
                ic(e)
                return Err("Please log in")

        privacy_result = self.read_repo.get_privacy(seller_id)

        return privacy_result
