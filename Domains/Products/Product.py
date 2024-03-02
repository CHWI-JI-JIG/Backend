import __init__
from dataclasses import dataclass
from abc import ABCMeta, abstractmethod
from typing import Optional, Self
from datetime import datetime

from Commons.format import KOREA_TIME_FORMAT
from Domains.Members import MemberID
from Domains.Products import ProductID


@dataclass(frozen=True)
class Product:
    id: ProductID
    seller_id: MemberID
    name: str
    img_path: str
    price: int
    description: str
    register_day: datetime


class IProductBuilder(metaclass=ABCMeta):
    @abstractmethod
    def set_id(self, id: ProductID) -> Self: ...

    @abstractmethod
    def set_seller_id(self, id: MemberID) -> Self: ...

    @abstractmethod
    def set_name(self, name: str) -> Self: ...

    @abstractmethod
    def set_img_path(self, img_path: str) -> Self: ...

    @abstractmethod
    def set_price(self, price: int) -> Self: ...

    @abstractmethod
    def set_description(self, description: str) -> Self: ...

    @abstractmethod
    def set_register_day(self, time: datetime) -> Self: ...

    @abstractmethod
    def build(self) -> Product: ...
