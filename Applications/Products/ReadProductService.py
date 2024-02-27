import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional, Tuple, List
from result import Result, Ok, Err

from uuid import uuid4, UUID

from Domains.Members import *
from Domains.Sessions import *
from Domains.Products import *
from Builders.Members import *
from Repositories.Members import *
from Applications.Members.ExtentionMethod import hashing_passwd
from datetime import datetime, timedelta
from Repositories.Products import IGetableProduct

from icecream import ic


class ReadProductService:
    def __init__(
        self,
        get_product_repo: IGetableProduct,
    ):
        assert issubclass(
            type(get_product_repo), IGetableProduct
        ), "get_product_repo must be a class that inherits from IGetableProduct."

        self.product_repo = get_product_repo

    def get_product_by_create_date(
        self,
        page=0,
        size=10,
    ) -> Result[Tuple[int, List[Product]], str]:
        """_summary_

        Args:
            page (int, optional): _description_. Defaults to 0.
            size (int, optional): _description_. Defaults to 10.

        Returns:
            Result[Tuple[int,List[Product]], str]:
                Ok( int, list ): int=> count of list max, list=> result
                Err(str): reason of Fail
        """
        ...

    def get_product_by_seller_id(
        self,
        seller_id: str,
        page=0,
        size=10,
    ) -> Result[Tuple[int, List[Product]], str]:
        """_summary_
        Product to look up Products with the same seller_id.

        Returns:
            Result[Tuple[int,List[Product]], str]:
                Ok( int, list ): int=> count of list max, list=> result
                Err(str): reason of Fail
        """
        ...
