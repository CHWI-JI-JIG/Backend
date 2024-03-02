import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional, Tuple, List
from result import Result
from uuid import UUID

from Applications.Payments import PayData


class IPaymentRepo(metaclass=ABCMeta):
    @abstractmethod
    def save_pay_data(self, data: PayData) -> Result[PayData, str]: ...
    @abstractmethod
    def load_pay_data(self, id: UUID) -> Optional[PayData]: ...
    @abstractmethod
    def load_list_of_pay_data(
        self,
        seller_name: Optional[str] = None,
        buyer_name: Optional[str] = None,
        page=0,
        size=10,
    ) -> Result[Tuple[int, List[PayData]], str]: ...
