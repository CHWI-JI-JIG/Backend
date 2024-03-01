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

    def read_privacy(
        self,
        user_session_key: str,
    ) -> Result[Privacy, str]: ...
