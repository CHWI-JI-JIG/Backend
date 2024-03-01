import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional, Tuple, List
from result import Result

from Domains.Members import *


class IReadableMember(metaclass=ABCMeta):
    @abstractmethod
    def get_privacy(self, member_id: MemberID) -> Result[Privacy, str]: ...
