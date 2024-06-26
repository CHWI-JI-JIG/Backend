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
from Builders.Products import *
from Builders.Comments import *
from Applications.Sessions.SessionHelper import check_valide_session

from icecream import ic


class CreateCommentService:
    def __init__(
        self,
        # read_member_repo: IReadableMember,
        save_comment: ISaveableComment,
        load_session: ILoadableSession,
    ):
        assert issubclass(
            type(save_comment), ISaveableComment
        ), "save_member_repo must be a class that inherits from ISaveableComment."

        self.comment_repo = save_comment

        assert issubclass(
            type(load_session), ILoadableSession
        ), "save_member_repo must be a class that inherits from ILoadableSession."

        self.load_session_repo = load_session
        

    def create_question(
        self,
        question : str,
        product_id: str,
        user_key: str,
    ) -> Result[CommentID, str]:
        builder = MemberSessionBuilder().set_deserialize_key(user_key)
        match self.load_session_repo.load_session(user_key):
                case Ok(json):
                    match builder.set_deserialize_value(json):
                        case Ok(session):
                            user_session = session.build()
                            if not check_valide_session(user_session):
                                return Err("만료된 세션입니다")
                        case _:
                            return Err("Invalid Member Session")
                case e:
                    return Err("만료된 세션입니다")
        match (
            CommentIDBuilder().set_uuid().map(lambda b:b.build()),
            ProductIDBuilder().set_uuid(product_id).map(lambda b:b.build()),
        ):
            case Ok(cid), Ok(pid):
                return self.comment_repo.save_comment(
                    Comment(
                        id = cid,
                        product_id= pid,
                        writer_id=user_session.member_id,
                        writer_account = "",
                        answer= None,
                        question=question,    
                    )
                )
            case c,p:
                ic()
                ic(c,p)
                assert False, f"c:{c} / p:{p}"
                return Err("Not Convert ID")
    
    def add_answer(
        self,
        answer: str,
        comment_id: str,
        user_key: str,
    ) -> Result[CommentID, str]:
        builder = MemberSessionBuilder().set_deserialize_key(user_key)
        match self.load_session_repo.load_session(user_key):
                case Ok(json):
                    match builder.set_deserialize_value(json):
                        case Ok(session):
                            user_session = session.build()
                            if not check_valide_session(user_session):
                                return Err("만료된 세션입니다")
                        case _:
                            return Err("Invalid Member Session")
                case _:
                    return Err("만료된 세션입니다")
    
        match CommentIDBuilder().set_uuid(comment_id).map(lambda b:b.build()) :
            case Ok(cid):
                return self.comment_repo.update_answer(
                    Comment_id=cid,
                    answer= answer,
                    member_id=user_session.member_id,
                )
            case c:
                ic()
                ic(c)
                assert False, f"c:{c}"
                return Err("Not Convert ID")