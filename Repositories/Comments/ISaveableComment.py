import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional
from result import Result
from uuid import UUID

from Domains.Members import *
from Domains.Comments import *


class ISaveableComment(metaclass=ABCMeta):
    @abstractmethod
    def save_comment(
        self, Comment: Comment
    ) -> Result[CommentID, str]: ...
    
    @abstractmethod
    def update_comment(self, Comment_id: CommentID, anwser:str,) -> Result[CommentID, str]:...
    
    
