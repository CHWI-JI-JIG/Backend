import __init__
from dataclasses import dataclass
from abc import ABCMeta, abstractmethod
from typing import Optional, Self
from datetime import datetime
import pytz

from Commons.format import KOREA_TIME_FORMAT
from Domains.Members import MemberID


@dataclass(frozen=True)
class Authentication:
    id: MemberID
    last_access: datetime
    fail_count: int
    is_sucess: bool

    def str_last_access(self, timezone: str = "UTC") -> str:
        match timezone.lower():
            case "utc":
                time = self.last_access.isoformat()
            case "asia/seoul" | "korea" | "korean" | "k":
                tz = pytz.timezone("Asia/Seoul")
                time = (
                    self.last_access.replace(tzinfo=tz)
                    .astimezone(tz)
                    .strftime(KOREA_TIME_FORMAT)
                )
            case _:
                assert False, "There are only two timezones: UTC or Korea time."
        return time


class IAuthenticationBuilder(metaclass=ABCMeta):
    @abstractmethod
    def set_id(self, id: MemberID) -> Self: ...

    @abstractmethod
    def set_last_access(self, time: datetime) -> Self: ...

    @abstractmethod
    def set_fail_count(self, cnt: int) -> Self: ...

    @abstractmethod
    def build(self) -> Authentication: ...
