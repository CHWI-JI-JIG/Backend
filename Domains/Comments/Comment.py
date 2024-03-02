import __init__
from dataclasses import dataclass
from abc import ABCMeta, abstractmethod
from typing import Optional, Self
from datetime import datetime

from Commons.format import KOREA_TIME_FORMAT
from Domains.Members import MemberID
from Domains.Products import ProductID
from Domains.Comments import CommentID


@dataclass(frozen=True)
class Comment:
    id: CommentID
    product_id: ProductID
    writer_id: MemberID
    writer_account: str
    answer: Optional[str]
    question: str


class ICommentBuilder(metaclass=ABCMeta):
    @abstractmethod
    def set_id(self, id: CommentID) -> Self: ...

    @abstractmethod
    def set_product_id(self, id: ProductID) -> Self: ...

    @abstractmethod
    def set_writer_id(self, id: MemberID) -> Self: ...

    @abstractmethod
    def set_writer_account(self, writer_account: str) -> Self: ...

    @abstractmethod
    def set_question(self, question: str) -> Self: ...

    @abstractmethod
    def set_answer(self, answer: str) -> Self: ...

    @abstractmethod
    def build(self) -> Comment: ...
