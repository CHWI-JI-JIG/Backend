import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional
from result import Result
from uuid import UUID

from Domains.Members import *
from Domains.Sessions import *


class ISaveableOrderTransition(metaclass=ABCMeta):
    @abstractmethod
    def save_order_transition(
        self, transition: OrderTransitionSession
    ) -> Result[OrderTransitionSession, str]:
        """
        Read User table. Make MemberSession. Save MemberSession

        Returns:
            Result[OrderTransitionSession, str]:
                Ok(order_transition): Sucess to Save transition
                Err(e) : db Error
        """
        ...
        
    def update_order_transition(
        self, transition: OrderTransitionSession
    ) -> Result[OrderTransitionSession, str]:
        ...
    
