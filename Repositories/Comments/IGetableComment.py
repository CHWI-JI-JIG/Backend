import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional, List, Tuple
from result import Result
from uuid import UUID

from Domains.Members import *
from Domains.Products import *
from Domains.Comments import *


class IGetableComment(metaclass=ABCMeta):
    @abstractmethod
    def get_comment_by_comment_id(self, comment_id: CommentID) -> Optional[Comment]: ...

    @abstractmethod
    def get_comments_by_product_id(
        self,
        product_id: ProductID,
        page=0,
        size=10,
    ) -> Result[Tuple[int, List[Comment]], str]:
        """_summary_

        Args:
            page (int, optional): _description_. Defaults to 0.
            size (int, optional): _description_. Defaults to 10.

        Returns:
            Result[Tuple[int,List[Comment]], str]:
                Ok( int, list ): int=> count of list max, list=> result
                Err(str): reason of Fail
        """

    @abstractmethod
    def get_comments_by_seller_id(
        self,
        seller_id: MemberID,
        page=0,
        size=10,
    ) -> Result[Tuple[int, List[Comment]], str]:
        """_summary_
        Comment to look up Comments with the same seller_id.

        Returns:
            Result[Tuple[int,List[Comment]], str]:
                Ok( int, list ): int=> count of list max, list=> result
                Err(str): reason of Fail
        """

    @abstractmethod
    def get_comments_by_writer_id(
        self,
        writer_id: MemberID,
        page=0,
        size=10,
    ) -> Result[Tuple[int, List[Comment]], str]:
        """_summary_
        Get Comments with the same writer_id.

        Returns:
            Result[Tuple[int,List[Comment]], str]:
                Ok( int, list ): int=> count of list max, list=> result
                Err(str): reason of Fail
        """
