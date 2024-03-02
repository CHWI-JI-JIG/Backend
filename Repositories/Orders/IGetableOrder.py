import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional, List, Tuple
from result import Result
from uuid import UUID

from Domains.Members import *
from Domains.Orders import *


class IGetableOrder(metaclass=ABCMeta):
    @abstractmethod
    def get_order_by_order_id(self, order_id: OrderID) -> Optional[Order]: ...

    @abstractmethod
    def get_orders_by_seller_id(
        self,
        seller_id: MemberID,
        page=0,
        size=10,
    ) -> Result[Tuple[int, List[Order]], str]:
        """_summary_
        Order to look up orders with the same seller_id.

        Returns:
            Result[Tuple[int,List[Product]], str]:
                Ok( int, list ): int=> count of list max, list=> result
                Err(str): reason of Fail
        """
        ...

    @abstractmethod
    def get_orders_by_buyer_id(
        self,
        buyer_id: MemberID,
        page=0,
        size=10,
    ) -> Result[Tuple[int, List[Order]], str]:
        """_summary_
        Get Orders with the same buyer_id.

        Returns:
            Result[Tuple[int,List[Product]], str]:
                Ok( int, list ): int=> count of list max, list=> result
                Err(str): reason of Fail
        """
        ...
