import __init__
from dataclasses import dataclass
from abc import ABCMeta, abstractmethod
from typing import Optional, Self
from enum import Enum
from datetime import datetime
from uuid import UUID, uuid4

from Domains import ID
from Domains.Members import *


@dataclass(frozen=True)
class PayData(ID):
    id: UUID
    seller_bank_account: str
    seller_id: MemberID
    seller_name: str
    buyer_card_account: str
    buyer_id: MemberID
    buyer_name: str
    transfer_time: datetime
    withdrawal: int
    deposit: int

    def get_id(self) -> str:
        return self.id.hex
