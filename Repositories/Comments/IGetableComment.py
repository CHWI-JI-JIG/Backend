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
    def get_comments_by_product_id( # product_id를 넣으면 모든 페이지의 comments 모두 가져온다) 페이지 단위로 comments를 가져온다
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
                Ok( int, list ): int=> count of list max, list=> result # list 개수 필수 for n개의 페이지까지 가져올 수 있기 때문이다. 
                Err(str): reason of Fail
        """
        ...
