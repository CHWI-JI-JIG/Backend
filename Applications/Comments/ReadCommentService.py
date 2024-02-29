import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional, Tuple, List
from result import Result, Ok, Err
from datetime import datetime, timedelta

from uuid import uuid4, UUID

from Commons.helpers import check_hex_string
from Domains.Members import *
from Domains.Comments import *
from Domains.Sessions import *
from Domains.Products import *

from Builders.Members import *
from Builders.Products import *


from Repositories.Members import *
from Repositories.Products import IGetableProduct
from Repositories.Comments import *
from Repositories.Sessions import ILoadableSession

from icecream import ic


class ReadOrderService:
    def __init__(
        self,
        get_comment_repo: IGetableComment,
    ):
        assert issubclass(
            type(get_comment_repo), IGetableProduct
        ), "get_product_repo must be a class that inherits from IGetableProduct."

        self.comment_repo = get_comment_repo
        

    def get_comment_data_for_product_page(
        self,
        product_id: str,
        page=0,
        size=10,
    ) -> Result[Tuple[int, List[Comment]], str]:
        """_summary_

        Args:
            page (int, optional): _description_. Defaults to 0.
            size (int, optional): _description_. Defaults to 10.

        Returns:
            Result[Tuple[int,List[comment]], str]:
                Ok( int, list ): int=> count of list max, list=> result
                Err(str): reason of Fail
        """
        ic()
        ic("코멘트 확인안했음")
        product_id = ProductIDBuilder().set_uuid(product_id).build()
        return self.comment_repo.get_comments_by_product_id(
            product_id=product_id, 
            page=page,
            size=size,
        )
