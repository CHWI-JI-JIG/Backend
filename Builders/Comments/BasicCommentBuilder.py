import __init__
from typing import Optional, Self, List, Union, Callable
from uuid import uuid4, UUID
from datetime import datetime

from Commons.helpers import check_hex_string
from Commons.format import KOREA_TIME_FORMAT

from Domains.Comments import *
from Domains import IDBuilder

from icecream import ic


class CommentIDBuilder(ICommentIDBuilder, IDBuilder):
    def __init__(self):
        super().__init__()

    def build(self) -> CommentID:
        match (self.uuid, self.sequence):
            case (uuid, seq) if isinstance(uuid, UUID):
                if seq is None:
                    seq = -1

                return CommentID(
                    uuid=uuid,
                    sequence=seq,
                )
            case (None, None):
                assert False, "You didn't set the uuid and seqence."
            case (None, seq) if isinstance(seq, int):
                assert False, "You didn't set the uuid."
            case _:
                assert False, "Unknown Error"
