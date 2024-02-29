import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional, Tuple, List
from result import Result, Ok, Err
from datetime import datetime, timedelta

from uuid import uuid4, UUID

from Commons.helpers import check_hex_string
from Domains.Members import *
from Domains.Orders import *
from Domains.Sessions import *
from Domains.Products import *
from Builders.Members import *
from Builders.Products import *
from Applications.Members.ExtentionMethod import hashing_passwd
from Repositories.Members import *
from Repositories.Products import IGetableProduct
from Repositories.Orders import *
from Repositories.Sessions import ILoadableSession

from icecream import ic


class ReadOrderService:
    def __init__(
        self,
        get_order_repo: IGetableOrder,
        load_session_repo: ILoadableSession,
    ):
        assert issubclass(
            type(get_order_repo), IGetableOrder
        ), "get_order_repo must be a class that inherits from IGetableorder."

        self.order_repo = get_order_repo

        assert issubclass(
            type(load_session_repo), ILoadableSession
        ), "load_session_repo must be a class that inherits from ILoadableSession."
        self.session_repo = load_session_repo

    def get_order_data_for_buyer_page(
        self,
        buyer_key: str,
        page=0,
        size=10,
    ) -> Result[Tuple[int, List[Order]], str]:
        """_summary_

        Args:
            page (int, optional): _description_. Defaults to 0.
            size (int, optional): _description_. Defaults to 10.

        Returns:
            Result[Tuple[int,List[order]], str]:
                Ok( int, list ): int=> count of list max, list=> result
                Err(str): reason of Fail
        """
        ic()
        ic("아직 세션 검증 안했슴. memberid 아직 안만듬")

        return self.order_repo.get_orders_by_buyer_id(
            buyer_id=None,
            page=page,
            size=size,
        )

    def get_order_data_for_seller_page(
        self,
        seller_key: str,
        page=0,
        size=10,
    ) -> Result[Tuple[int, List[Order]], str]:
        """_summary_

        Args:
            page (int, optional): _description_. Defaults to 0.
            size (int, optional): _description_. Defaults to 10.

        Returns:
            Result[Tuple[int,List[order]], str]:
                Ok( int, list ): int=> count of list max, list=> result
                Err(str): reason of Fail
        """
        ic()
        ic("아직 세션 검증 안했슴. memberid 아직 안만듬")

        return self.order_repo.get_orders_by_seller_id(
            seller_id=None,
            page=page,
            size=size,
        )
