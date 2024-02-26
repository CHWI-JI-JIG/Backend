import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional
from result import Result
from uuid import UUID

from Domains.Members import *
from Domains.Products import *
from Domains.Comments import *


class ISaveableComment(mataclass=ABCMeta):
    @abstractmethod
    def save_comment(self, comment: Comment) -> Result[CommentID, str]: ...
