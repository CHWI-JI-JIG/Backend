import __init__
from dataclasses import dataclass
from abc import *
from typing import Optional, Self

from Domains.Members import MemberID


@dataclass(frozen=True)
class Privacy:
    """_summary_
    Args:
        company_registration_number: seller(str) / buyer(None) / admin(None)
    """

    id: MemberID
    name: str
    phone: str
    email: str
    address: str
    company_registration_number: Optional[str] = None


class IPrivacyBuilder(metaclass=ABCMeta):
    @abstractmethod
    def set_id(self, id: MemberID) -> Self: ...

    @abstractmethod
    def set_name(self, name: str) -> Self: ...

    @abstractmethod
    def set_phone(self, phone: str) -> Self: ...

    @abstractmethod
    def set_email(self, email: str) -> Self: ...

    @abstractmethod
    def set_address(self, address: str) -> Self: ...

    @abstractmethod
    def set_company_registration_number(
        self, company_registration_number: str
    ) -> Self: ...

    @abstractmethod
    def build(self) -> Privacy: ...
