import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional
from result import Result, Ok, Err

from Domains.Members import *
from Domains.Products import *
from Domains.Orders import *
from Domains.Sessions import *
from Builders.Members import *

from Repositories.Members import *
from Repositories.Products import *
from Repositories.Orders import *
from Repositories.Products import *
from Repositories.Sessions import *

from icecream import ic


class OrderPaymentService:
    """
    할일
    1. 결제로 갈때, 주문 정보를 담고 있는 트렌젝션을 저장하고, 트렌젝션을 발급해준다.
    # 2. 유효한 결제 정보인지 확인한다.
    # 3. 결제가 완료되면, 결제정보가 맞는지 검증세션을 확인해서, 유효한 결제 정보인지 확인한다.
    3. 결제 창에서 True 값이 넘어면,
    4. 유효한 결제 정보라면, 주문 트렌젝션을 불러와서 결제를 진행한다.
    """

    def __init__(
        self,
        save_order: ISaveableOrder,
        save_transition: ISaveableOrderTransition,
        load_session: ILoadableSession,
    ):
        assert issubclass(
            type(save_order), ISaveableOrder
        ), "save_member_repo must be a class that inherits from ISaveableOrder."

        self.order_repo = save_order

        assert issubclass(
            type(save_transition), ISaveableOrderTransition
        ), "save_member_repo must be a class that inherits from ISaveableOrderTransition."

        self.transition_repo = save_transition

        assert issubclass(
            type(load_session), ILoadableSession
        ), "save_member_repo must be a class that inherits from ILoadableSession."

        self.load_repo = load_session

    def publish_order_transition(
        self,
        recipient_name: str,
        recipient_phone: str,
        recipient_address: str,
        product_id: str,
        buy_count: int,
        single_price: int,
        user_session_key: str,
    ) -> Result[OrderTransitionSession, str]:
        # check member session
        builder = MemberSessionBuilder().set_deserialize_key(user_session_key)
        match self.load_repo.load_session(user_session_key):
            case Ok(json):
                match builder.set_deserialize_value(json):
                    case Ok(session):
                        user_session = session.build()
                        buyer_id = user_session.member_id.get_id()
                    case _:
                        return Err("Invalid Member Session")
            case _:
                return Err("plz login")

        # publish
        return self.transition_repo.save_order_transition(
            OrderTransitionBuilder()
            .set_key()
            .set_recipient_name(recipient_name)
            .set_recipient_phone(recipient_phone)
            .set_recipient_address(recipient_address)
            .set_product_id(product_id)
            .set_buyer_id(buyer_id)
            .set_count_and_price(
                buy_count=buy_count,
                price=single_price,
            )
            .build()
        )

    def payment_and_approval_order(
        self,
        order_transition_session: str,
        payment_success: bool,
    ) -> Result[OrderID, str]:
        # load transition
        bulider = OrderTransitionBuilder().set_deserialize_key(order_transition_session)
        match self.load_repo.load_session(order_transition_session):
            case Ok(json):
                match bulider.set_deserialize_value(json):
                    case Ok(session):
                        order_session = session.set_is_success(payment_success).build()
                    case e:
                        ic(e)
                        return Err("Invalid Order Transition")
            case e:
                ic(e)
                return Err("Not Exists Session")

        # payment order
        match order_session.is_success:
            case True:
                return self.order_repo.save_order(order=order_session.order)
            case _:
                return Err("Fail Payment")
