import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional, List, Tuple
from result import Result
from uuid import UUID

from Domains.Members import *
from Domains.Products import *


class IGetableProduct(metaclass=ABCMeta):
    @abstractmethod
    def get_product_by_product_id(self, product_id: ProductID) -> Optional[Product]: ...

    @abstractmethod
    def get_products_by_create_date(
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

    @abstractmethod
    def get_products_by_seller_id(
        self,
        seller_id: MemberID,
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

    @abstractmethod
    def get_products_by_buyer_id_from_order(
        self,
        buyer_id: MemberID,
        page=0,
        size=10,
    ) -> Result[Tuple[int, List[Product]], str]:
        """_summary_
        Get Products with the same buyer_id from an order.

        Returns:
            Result[Tuple[int,List[Product]], str]:
                Ok( int, list ): int=> count of list max, list=> result
                Err(str): reason of Fail
        """
        ...
