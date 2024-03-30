import __init__
from dataclasses import dataclass
from abc import ABCMeta, abstractmethod
from typing import Optional, Self, Union
from uuid import uuid4, UUID
import json
from pathlib import Path
from result import Result, Err, Ok
from datetime import datetime

from Commons.helpers import check_hex_string

from Domains import ID
from Domains.Sessions import (
    ISessionSerializeable,
    ISessionBuilder,
    SecuritySession,
    SecuritySessionBuilder,
    SessionToken,
)
from Domains.Products import *
from Domains.Members import *
from Domains.Orders import *


from Builders.Members import *
from Builders.Products import *
from Builders.Orders import *

from icecream import ic


@dataclass(frozen=True)
class OrderTransitionSession(ID, ISessionSerializeable, SecuritySession):
    order: Order
    is_success: Optional[bool] = None

    max_count: int = 3
    minute: int = 3

    def MAX_USE_COUNT(self) -> int:
        return self.max_count

    def VALIDE_MINUTE(self) -> int:
        return self.minute

    def get_id(self) -> str:
        return self.get_key()

    def serialize_key(self) -> str:
        return self.get_id()

    def serialize_value(self) -> str:
        order = self.order
        assert (
            isinstance(self.is_success, bool) or self.is_success is None
        ), "Type of is_succuss is bool."
        match self.is_success:
            case None:
                return json.dumps(
                    {
                        "check_success": False,
                        "buyer_id": order.buyer_id.get_id(),
                        "recipient_name": order.recipient_name,
                        "recipient_phone": order.recipient_phone,
                        "recipient_address": order.recipient_address,
                        "product_id": order.product_id.get_id(),
                        "buy_count": order.buy_count,
                        "total_price": order.total_price,
                    },
                    ensure_ascii=False,
                )
            case is_success:
                assert isinstance(is_success, bool), "Type of is_success is bool."
                return json.dumps(
                    {
                        "check_success": True,
                        "is_success": is_success,
                        "buyer_id": order.buyer_id.get_id(),
                        "recipient_name": order.recipient_name,
                        "recipient_phone": order.recipient_phone,
                        "recipient_address": order.recipient_address,
                        "product_id": order.product_id.get_id(),
                        "buy_count": order.buy_count,
                        "total_price": order.total_price,
                    },
                    ensure_ascii=False,
                )


class OrderTransitionBuilder(ISessionBuilder, SecuritySessionBuilder):
    def __init__(
        self,
        recipient_name: Optional[str] = None,
        recipient_phone: Optional[str] = None,
        recipient_description: Optional[str] = None,
        owner_id: Optional[UUID] = None,
        use_count: Optional[int] = None,
        create_time: Optional[datetime] = None,
    ):
        super().__init__(
            key=None,
            owner_id=owner_id,
            use_count=use_count,
            create_time=create_time,
        )
        self.buyer_id: Optional[MemberID] = None
        self.recipient_name: Optional[str] = recipient_name
        self.recipient_phone = recipient_phone
        self.recipient_address = recipient_description
        self.product_id: Optional[ProductID] = None
        self.buy_count: Optional[int] = None
        self.total_price: Optional[int] = None
        self.is_success: Optional[bool] = None

    def set_deserialize_key(self, key: str) -> Self:
        self.set_key(key)
        return self

    def set_deserialize_value(self, token: SessionToken) -> Result[Self, str]:
        assert isinstance(token, SessionToken), "Type of token is SessionToken."
        try:
            to_dict = json.loads(token.value)
        except:
            return Err("fail read json")
        assert isinstance(to_dict, dict), "Type of convert value is Dict."

        dict_key = "check_success"
        if not isinstance(to_dict.get(dict_key), bool):
            return Err(f"Not Exists {dict_key}")
        if to_dict.get(dict_key):
            dict_key = "is_success"
            if not isinstance(to_dict.get(dict_key), bool):
                return Err(f"Not Exists {dict_key}")
            self.set_is_success(to_dict.get(dict_key))

        dict_key = "buyer_id"
        if not isinstance(to_dict.get(dict_key), str):
            return Err(f"Not Exists {dict_key}")
        self.set_buyer_id(to_dict.get(dict_key))

        dict_key = "recipient_name"
        if not isinstance(to_dict.get(dict_key), str):
            return Err(f"Not Exists {dict_key}")
        self.set_recipient_name(to_dict.get(dict_key))

        dict_key = "recipient_phone"
        if not isinstance(to_dict.get(dict_key), str):
            return Err(f"Not Exists {dict_key}")
        self.set_recipient_phone(to_dict.get(dict_key))

        dict_key = "recipient_address"
        if not isinstance(to_dict.get(dict_key), str):
            return Err(f"Not Exists {dict_key}")
        self.set_recipient_address(to_dict.get(dict_key))

        dict_key = "product_id"
        if not isinstance(to_dict.get(dict_key), str):
            return Err(f"Not Exists {dict_key}")
        self.set_product_id(to_dict.get(dict_key))

        dict_key = "buy_count"
        if not isinstance(to_dict.get(dict_key), int):
            return Err(f"Not Exists {dict_key}")

        self.set_count(to_dict.get(dict_key))

        dict_key = "total_price"
        if not isinstance(to_dict.get(dict_key), int):
            return Err(f"Not Exists {dict_key}")
        self.set_total_price(to_dict.get(dict_key))

        return (
            self.set_use_count(token.use_count)
            .set_create_time(token.create_time)
            .set_owner_id(token.owner_id)
        )

    def check_set_success(self) -> bool:
        return isinstance

    def set_is_success(self, is_success: bool) -> Self:
        assert self.is_success is None, "The is_success is already set."
        assert isinstance(is_success, bool), "Type of is_success is bool."
        self.is_success = is_success

        return self

    def set_recipient_name(self, name: str) -> Self:
        assert self.recipient_name is None, "name is already set."
        assert isinstance(name, str), "Type of name is str"

        self.recipient_name = name
        return self

    def set_recipient_phone(self, phone: str) -> Self:
        assert self.recipient_phone is None, "phone is already set."
        assert isinstance(phone, str), "Type of phone is str"

        self.recipient_phone = phone
        return self

    def set_recipient_address(self, recipient_address: str) -> Self:
        assert self.recipient_address is None, "recipient_address is already set."
        assert isinstance(recipient_address, str), "Type of recipient_address is str."

        self.recipient_address = recipient_address
        return self

    def set_count_and_price(self, buy_count: int, price: int) -> Self:
        assert isinstance(price, int), "Type of price is int."
        assert isinstance(buy_count, int), "Type of buy_count is int."
        assert self.total_price is None, "The price is already set."
        assert self.buy_count is None, "The buy_count is already set."
        assert price >= 100, "price >= 0"
        assert buy_count >= 1, "count >= 0"

        self.buy_count = buy_count
        self.total_price = price * buy_count
        return self

    def set_count(self, buy_count: int) -> Self:
        assert isinstance(buy_count, int), "Type of buy_count is int."
        assert self.total_price is None, "The price is already set."
        assert buy_count >= 1, "count >= 0"

        self.buy_count = buy_count
        return self

    def set_total_price(self, total_price: int) -> Self:
        assert isinstance(total_price, int), "Type of total price is int."
        assert self.total_price is None, "The price is already set."
        assert total_price >= 100, "price >= 0"

        self.total_price = total_price
        return self

    def set_buyer_id(self, buyer_id: Union[UUID, str]) -> Result[Self, str]:
        assert self.buyer_id is None, "buyer id is already set."

        match MemberIDBuilder().set_uuid(buyer_id).map(lambda b: b.build()):
            case Ok(id):
                id = id
            case e:
                return e

        assert isinstance(
            id, MemberID
        ), "ValueType Error: Initialize the id via MemberIDBuilder."

        self.buyer_id = id
        return Ok(self)

    def set_product_id(self, product_id: str) -> Result[Self, str]:
        assert self.product_id is None, "product id is already set."
        assert isinstance(product_id, str), "Type of product_id is str."
        assert check_hex_string(product_id), "The product is not in hex format."

        match ProductIDBuilder().set_uuid(product_id).map(lambda b: b.build()):
            case Ok(id):
                id = id
            case e:
                return e

        assert isinstance(
            id, ProductID
        ), "ValueType Error: Initialize the id via ProductIDBuilder."

        self.product_id = id
        return Ok(self)

    def build(self) -> Result[OrderTransitionSession, str]:
        key = "key"
        assert isinstance(self.key, UUID), f"Not Set {key}."
        key = "buyer_id"
        assert isinstance(self.buyer_id, MemberID), f"Not Set {key}."
        key = "recipient_name"
        assert isinstance(self.recipient_name, str), f"Not Set {key}."
        key = "recipient_phone"
        assert isinstance(self.recipient_phone, str), f"Not Set {key}."
        key = "recipient_address"
        assert isinstance(self.recipient_address, str), f"Not Set {key}."
        key = "product_id"
        assert isinstance(self.product_id, ProductID), f"Not Set {key}."
        key = "buy_count"
        assert isinstance(self.buy_count, int), f"Not Set {key}."
        key = "total_price"
        assert isinstance(self.total_price, int), f"Not Set {key}."
        self.assert_and_check_about_setting()

        match OrderIDBuilder().set_uuid(self.key).map(lambda b: b.build()):
            case Ok(oid):
                return Ok(
                    OrderTransitionSession(
                        key=self.key,
                        order=Order(
                            id=oid,
                            product_id=self.product_id,
                            buyer_id=self.buyer_id,
                            recipient_name=self.recipient_name,
                            recipient_phone=self.recipient_phone,
                            recipient_address=self.recipient_address,
                            product_name="dump",
                            product_img_path="dump",
                            buy_count=self.buy_count,
                            total_price=self.total_price,
                            order_date=datetime.now(),
                        ),
                        owner_id=self.owner_id,
                        create_time=self.create_time,
                        use_count=self.use_count,
                        is_success=self.is_success,
                    )
                )
            case e:
                return e
