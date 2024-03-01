import __init__
from dataclasses import dataclass
from abc import ABCMeta, abstractmethod
from typing import Optional, Self
from uuid import uuid4, UUID
import json
from pathlib import Path
from result import Result, Err, Ok
from datetime import datetime

from Commons.helpers import check_hex_string

from Domains import ID
from Domains.Products import *
from Domains.Sessions import ISessionSerializeable, ISesseionBuilder
from Domains.Members import *
from Domains.Orders import *


from Builders.Members import *
from Builders.Products import *
from Builders.Orders import *

from icecream import ic


@dataclass(frozen=True)
class OrderTransitionSession(ID, ISessionSerializeable):
    key: UUID
    order: Order

    def get_id(self) -> str:
        return self.key.hex

    def serialize_key(self) -> str:
        return self.get_id()

    def serialize_value(self) -> str:
        order = self.order
        return json.dumps(
            {
                "buyer_id": order.buyer_id.get_id(),
                "recipient_name": order.recipient_name,
                "recipient_phone": order.recipient_phone,
                "recipient_address": order.recipient_address,
                "product_id": order.product_id,
                "buy_count": order.buy_count,
                "total_price": order.total_price,
            },
            ensure_ascii=False,
        )


class ProductSessionBuilder(ISesseionBuilder):
    def __init__(
        self,
        recipient_name: Optional[str] = None,
        recipient_phone: Optional[str] = None,
        recipient_description: Optional[str] = None,
    ):
        self.key: Optional[UUID] = None
        self.buyer_id: Optional[MemberID] = None
        self.recipient_name: Optional[str] = recipient_name
        self.recipient_phone = recipient_phone
        self.recipient_address = recipient_description
        self.product_id: Optional[ProductID] = None
        self.buy_count: Optional[int] = None
        self.total_price: Optional[int] = None

    def set_deserialize_key(self, key: str) -> Self:
        self.set_key(key)
        return self

    def set_deserialize_value(self, value: str) -> Result[Self, str]:
        assert isinstance(value, str), "Type of value is str."
        try:
            to_dict = json.loads(value)
        except:
            return Err("fail read json")
        assert isinstance(to_dict, dict), "Type of convert value is Dict."

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

        return Ok(self)

    def set_key(self, key: Optional[str] = None) -> Self:
        assert self.key is None, "The Key is already set."
        match key:
            case None:
                self.key = uuid4()
            case k if isinstance(key, str):
                assert check_hex_string(k), "The uuid_hex is not in hex format."
                self.key = UUID(hex=key)
            case _:
                assert False, "Type of key is str."
        assert isinstance(self.key, UUID), "Not set key."

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

    def set_count(self, buy_count: int, price: int) -> Self:
        assert isinstance(buy_count, int), "Type of buy_count is int."
        assert self.total_price is None, "The price is already set."
        assert buy_count >= 1, "count >= 0"

        self.buy_count = buy_count
        self.total_price = price * buy_count
        return self

    def set_total_price(self, total_price: int) -> Self:
        assert isinstance(total_price, int), "Type of total price is int."
        assert self.total_price is None, "The price is already set."
        assert total_price >= 100, "price >= 0"

        self.total_price = total_price
        return self

    def set_buyer_id(self, buyer_id: str) -> Self:
        assert self.buyer_id is None, "buyer id is already set."
        assert isinstance(buyer_id, str), "Type of buyer_id is str."
        assert check_hex_string(buyer_id), "The buyer is not in hex format."

        id = MemberIDBuilder().set_uuid(buyer_id).build()

        assert isinstance(
            id, MemberID
        ), "ValueType Error: Initialize the id via MemberIDBuilder."

        self.buyer_id = id
        return self

    def set_img_path(self, img_path: str) -> Result[Self, str]:
        from Commons.format import IMG_PATH
        import os.path

        assert self.img_path is None, "img path is already set."
        # assert os.path.isfile(
        #     IMG_PATH / img_path
        # ), f"Not Exsist '{str(IMG_PATH/img_path)}'. img path is not abs path."

        if not os.path.isfile(IMG_PATH / img_path):
            ic()
            print("Not Implement")
            print(f"Not Exsist '{str(IMG_PATH/img_path)}'. img path is not abs path.")
            # return Err(f"Not Exsist '{str(IMG_PATH/img_path)}'. img path is not abs path.")

        self.img_path = img_path
        return Ok(self)

    def build(self) -> ProductTempSession:
        assert isinstance(self.seller_id, MemberID), "Not Set seller_id"

        match (self.name, self.price, self.description, self.seller_id):
            case (None, None, None, _):
                product = None
            case (name, price, description, seller_id) if (
                isinstance(name, str)
                and isinstance(price, int)
                and isinstance(description, str)
                and isinstance(seller_id, MemberID)
            ):
                id = ProductIDBuilder().set_uuid().build()
                product = Product(
                    id=id,
                    seller_id=seller_id,
                    name=name,
                    description=description,
                    img_path="Dump",
                    register_day=datetime.now(),
                    price=price,
                )
            case _:
                assert False, "Not Set name, price, description, seller_id."

        match self.img_path:
            case None:
                img_path = ""
            case img_path if isinstance(img_path, str):
                img_path = img_path
            case _:
                assert False, "img path don't set."

        return ProductTempSession(
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
        )
