import __init__
from dataclasses import dataclass
from abc import ABCMeta, abstractmethod
from typing import Optional, Self
from datetime import datetime

from Commons.format import KOREA_TIME_FORMAT
from Domains.Members import MemberID
from Domains.Products import ProductID
from Domains.Orders import OrderID


@dataclass(frozen=True)
class Order:
    id: OrderID
    product_id: ProductID
    buyer_id: MemberID
    count: int
    total_price: int
    order_date: datetime


class IOrderBuilder(metaclass=ABCMeta):
    @abstractmethod
    def set_id(self, id: OrderID) -> Self: ...

    @abstractmethod
    def set_product_id(self, id: ProductID) -> Self: ...

    @abstractmethod
    def set_buyer_id(self, id: MemberID) -> Self: ...

    @abstractmethod
    def set_count_and_price(self, count: int, price: int) -> Self: ...

    @abstractmethod
    def set_order_date(self, time: datetime) -> Self: ...

    @abstractmethod
    def build(self) -> Order: ...
