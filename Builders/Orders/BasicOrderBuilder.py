import __init__
from typing import Optional, Self, List, Union, Callable
from uuid import uuid4, UUID
from datetime import datetime

from Commons.helpers import check_hex_string
from Commons.format import KOREA_TIME_FORMAT

from Domains.Orders import *
from Domains.Products import *

from icecream import ic


class OrderIDBuilder(IOrderIDBuilder):
    def __init__(self):
        self.uuid: Optional[UUID] = None
        self.sequence: Optional[int] = None

    def set_seqence(self, seq: int) -> Self:
        assert isinstance(seq, int), "Type of seq is int."
        assert self.sequence is None, "The sequence is already set."
        assert seq >= 0, "seq >= 0"

        self.sequence = seq
        return self

    def set_uuid(self, uuid_hex: Optional[str] = None) -> Self:
        assert self.uuid is None, "The uuid_hex is already set."
        match uuid_hex:
            case None:
                self.uuid = uuid4()
            case k if isinstance(uuid_hex, str):
                assert check_hex_string(k), "The uuid_hex is not in hex format."
                self.uuid = UUID(hex=uuid_hex)
            case _:
                assert False, "Type of uuid_hex is str."

        return self

    def build(self) -> OrderID:
        match (self.uuid, self.sequence):
            case (uuid, seq) if isinstance(uuid, UUID):
                if seq is None:
                    seq = -1

                return OrderID(
                    uuid=uuid,
                    sequence=seq,
                )
            case (None, None):
                assert False, "You didn't set the uuid and seqence."
            case (None, seq) if isinstance(seq, int):
                assert False, "You didn't set the uuid."
            case _:
                assert False, "Unknown Error"
