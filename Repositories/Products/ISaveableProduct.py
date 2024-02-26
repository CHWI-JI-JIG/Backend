import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional
from result import Result
from uuid import UUID

from Domains.Members import *
from Domains.Products import *


class ISaveableProduct(metaclass=ABCMeta):
    @abstractmethod
    def save_product(self, product: Product) -> Result[ProductID, str]: ...
