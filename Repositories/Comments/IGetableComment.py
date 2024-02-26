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
        ...
