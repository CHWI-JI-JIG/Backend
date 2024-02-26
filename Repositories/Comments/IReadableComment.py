import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional, Tuple
from result import Result

from Domains.Comments import *
from Domains.Members import *


class IReadableComment(metaclass=ABCMeta):
    @abstractmethod
    def check_exist_comment(self, account: str) -> bool: ...

    @abstractmethod
    def get_comment(self, member_id: CommentID) -> Result[CommentID, str]: ...

    @abstractmethod
    def get_privacy(self, member_id: CommentID) -> Result[Privacy, str]: ...

    @abstractmethod
    def get_member_and_privacy(
        self, member_id: MemberID
    ) -> Result[Tuple[Member, Privacy], str]: ...

# GETABLE에 ID를 넣으면 COMMENT가 나오게 수정하려고 함. 
    # join을 해야 한다. 
    # comment 조회 시, 상품조회에 관련된 qna를 가져와야 한다. 