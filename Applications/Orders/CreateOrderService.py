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
    """
    할일
    1. 결제로 갈때, 주문 정보를 담고 있는 트렌젝션을 저장한다.
    # 2. 유효한 트렌젝션인지 확인한다.
    # 3. 결제가 완료되면, 결제정보가 맞는지 검증세션을 확인해서, 유효한 결제 정보인지 확인한다.
    3. 결제 창에서 True 값이 넘어면,
    4. 유효한 결제 정보라면, 주문 트렌젝션을 불러와서 결제를 진행한다.
    """

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

    def publish_temp_order_id(
        self,
        buyer_id:str,
        recipient_name:str,
        recipient_phone:str,
        recipient_address:str,
        product_id:str,
        buy_count:int,
        single_pricet:int,
        user_session_key:str,
    ) ->