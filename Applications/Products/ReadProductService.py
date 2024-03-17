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
from Repositories.Sessions import ILoadableSession

from icecream import ic


class ReadProductService:
    def __init__(
        self,
        get_product_repo: IGetableProduct,
        load_session_repo: ILoadableSession,
    ):
        assert issubclass(
            type(get_product_repo), IGetableProduct
        ), "get_product_repo must be a class that inherits from IGetableProduct."

        self.product_repo = get_product_repo

        assert issubclass(
            type(load_session_repo), ILoadableSession
        ), "load_session_repo must be a class that inherits from ILoadableSession."
        self.session_repo = load_session_repo

    def get_product_for_detail_page(
        self,
        product_id: str,
    ) -> Optional[Product]:
        assert check_hex_string(product_id), "The product_id is not in hex format."
        match ProductIDBuilder().set_uuid(product_id).map(lambda b: b.build()):
            case Ok(id):
                assert isinstance(id, ProductID), "Type of product_id is ProductID."
                return self.product_repo.get_product_by_product_id(product_id=id)
            case e:
                return e

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
        return self.product_repo.get_products_by_create_date(
            page=page,
            size=size,
        )

    def get_product_data_for_seller_page(
        self,
        user_key: str,
        page=0,
        size=10,
    ) -> Result[Tuple[int, List[Product]], str]:
        """_summary_
        Product to look up Products with the same seller_id.

        Returns:
            Result[Tuple[int,List[Product]], str]:
                Ok( int, list ): int=> count of list max, list=> result
                Err(str): reason of Fail
                    'NotExsistKey'
                    'NotOnwer'
        """
        builder = MemberSessionBuilder().set_deserialize_key(user_key)
        match self.session_repo.load_session(user_key):
            case Ok(json):
                match builder.set_deserialize_value(json):
                    case Ok(session):
                        user_session = session.build()
                        seller_id = user_session.member_id
                    case _:
                        return Err("Invalid Member Session")
            case _:
                return Err("plz login")

        assert isinstance(seller_id,MemberID), "Not MenberID."

        return self.product_repo.get_products_by_seller_id(
            seller_id=seller_id,
            page=page,
            size=size,
        )
