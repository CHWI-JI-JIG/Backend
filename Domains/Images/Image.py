import __init__
from dataclasses import dataclass
from abc import ABCMeta, abstractmethod
from typing import Optional, Self
from datetime import datetime

from Commons.format import KOREA_TIME_FORMAT
from Domains.Members import MemberID
from Domains.Products import ProductID
from Domains.Images import ImageID


@dataclass(frozen=True)
class ProductImage:
    id: ImageID
    product_id: ProductID
    img_path: str


class IProductBuilder(metaclass=ABCMeta):
    @abstractmethod
    def set_id(self, id: ImageID) -> Self: ...

    @abstractmethod
    def set_product_id(self, id: MemberID) -> Self: ...

    @abstractmethod
    def set_img_path(self, img_path: str) -> Self: ...

    @abstractmethod
    def build(self) -> ProductImage: ...
