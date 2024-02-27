import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional
from result import Result
from uuid import UUID

from Domains.Members import *
from Domains.Orders import *


class ISaveableOrder(metaclass=ABCMeta):
    @abstractmethod
    def save_order(self, order: Order) -> Result[OrderID, str]: ...
