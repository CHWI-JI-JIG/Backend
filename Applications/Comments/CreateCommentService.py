import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional
from result import Result, Ok, Err

from Domains.Members import *
from Domains.Products import *
from Domains.Comments import *
from Domains.Sessions import *
from Builders.Members import *
from Repositories.Members import *
from Repositories.Products import *
from Repositories.Comments import *
from Repositories.Sessions import *

from icecream import ic


class CreateCommentService:
    def __init__(
        self,
        # read_member_repo: IReadableMember,
        save_comment: ISaveableComment,
        load_session: ILoadableSession,
    ):
        assert issubclass(
            type(save_comment), ISaveableMember
        ), "save_member_repo must be a class that inherits from ISaveableMember."

        self.comment_repo = save_comment

        assert issubclass(
            type(load_session), ILoadableSession
        ), "save_member_repo must be a class that inherits from ILoadableSession."

        self.load_repo = load_session

    def create_question(
        self,
        product_id: str,
        user_key: str,
    ) -> Result[CommentID, str]: ...

    def Add_answer(
        self,
        comment_id: str,
        user_key: str,
    ) -> Result[CommentID, str]: ...
