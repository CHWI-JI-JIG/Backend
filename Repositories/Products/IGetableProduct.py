import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional, List
from result import Result
from uuid import UUID

from Domains.Members import *
from Domains.Products import *


class IGetableProduct(metaclass=ABCMeta):
    @abstractmethod
    def get_product_by_create_date(
        self,
        page=0,
        size=10,
    ) -> Result[List[Product], str]: ...
