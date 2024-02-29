import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional, Tuple, List
from result import Result

from Domains.Members import *

class IReadableMemberList(metaclass=ABCMeta):
    @abstractmethod
    def get_members(
        self,
        page=0,
        size=10,
    ) -> Result[Tuple[int, List[Member]], str]:
        """_summary_

        Args:
            page (int, optional): _description_. Defaults to 0.
            size (int, optional): _description_. Defaults to 10.

        Returns:
            Result[Tuple[int,List[Product]], str]:
                Ok( int, list ): int=> count of list max, list=> result
                Err(str): reason of Fail
        """
        ...
