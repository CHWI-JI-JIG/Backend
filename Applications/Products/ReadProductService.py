import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional, Tuple, List
from result import Result, Ok, Err

from uuid import uuid4, UUID

from Commons.helpers import check_hex_string
from Domains.Members import *
from Domains.Sessions import *
from Domains.Products import *
from Builders.Members import *
from Builders.Products import *
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

    def get_product_for_detail_page(
        self,
        product_id: str,
    ) -> Optional[Product]:
        assert check_hex_string(product_id), "The product_id is not in hex format."
        id = ProductIDBuilder().set_uuid(product_id).build()

        assert isinstance(id, MemberID), "Type of product_id is ProductID."

        return self.product_repo.get_product_by_product_id(seller_id=id)

    def get_product_data_for_main_page(
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
        return self.get_product_by_create_date(
            page=page,
            size=size,
        )

    def get_product_data_for_seller_page(
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
        assert check_hex_string(seller_id), "The seller_id is not in hex format."
        member_id = MemberIDBuilder().set_uuid(seller_id).build()

        assert isinstance(member_id, MemberID), "Type of seller_id is MemberID."

        return self.product_repo.get_products_by_seller_id(
            seller_id=member_id,
            page=page,
            size=size,
        )
