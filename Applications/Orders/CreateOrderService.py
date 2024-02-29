import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional
from result import Result, Ok, Err

from Domains.Members import *
from Domains.Products import *
from Domains.Comments import *
from Domains.Sessions import *
from Builders.Members import *
from Repositories.Members import *
from Repositories.Products import *
from Repositories.Orders import *
from Repositories.Products import *
from Repositories.Sessions import *

from icecream import ic


class CreateOrderService:
    def __init__(
        self,
        save_order: ISaveableOrder,
        load_session: ILoadableSession,
    ):
        assert issubclass(
            type(save_order), ISaveableMember
        ), "save_member_repo must be a class that inherits from ISaveableMember."

        self.order_repo = save_order

        assert issubclass(
            type(load_session), ILoadableSession
        ), "save_member_repo must be a class that inherits from ILoadableSession."

        self.load_repo = load_session
        
    def 
