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
from Domains.Sessions import ISessionSerializeable, ISesseionBuilder
from Domains import ID
from Domains.Members import *
from Builders.Members import *
from Builders.Products import *
from Domains.Products import *

from icecream import ic


@dataclass(frozen=True)
class ProductTempSession(ID, ISessionSerializeable):
    key: UUID
    product: Optional[Product]
    img: str = ""

    def get_id(self) -> str:
        return self.key.hex

    def serialize_key(self) -> str:
        return self.get_id()

    def serialize_value(self) -> str:
        match (self.product, self.img):
            case (p, i) if isinstance(p, Product) and len(i) > 0:
                return json.dumps(
                    {
                        "check_product": True,
                        "check_img": True,
                        "seller_id": p.seller_id,
                        "name": p.name,
                        "price": p.price,
                        "description": p.description,
                        "img": i,
                    },
                    ensure_ascii=False,
                )

            case (none, i) if len(i) > 0 and none is None:
                return json.dumps(
                    {
                        "check_product": False,
                        "check_img": True,
                        "img": i,
                    },
                    ensure_ascii=False,
                )
            case (p, none) if len(none) <= 0 and isinstance(p):
                return json.dumps(
                    {
                        "check_product": True,
                        "check_img": False,
                        "seller_id": p.seller_id,
                        "name": p.name,
                        "price": p.price,
                        "description": p.description,
                    },
                    ensure_ascii=False,
                )
            case _:
                return json.dumps(
                    {
                        "check_product": False,
                        "check_img": False,
                    },
                    ensure_ascii=False,
                )


class MemberSessionBuilder(ISesseionBuilder):
    def __init__(
        self,
        key: Optional[UUID] = None,
        name: Optional[str] = None,
        price: Optional[int] = None,
        description: Optional[str] = None,
        img_path: Optional[str] = None,
    ):
        self.key = key
        self.seller_id: Optional[MemberID] = None
        self.name: Optional[name] = name
        self.price = price
        self.description = description
        self.img_path = img_path

    def set_deserialize_key(self, key: str) -> Self:
        self.set_key(key)
        return self

    def set_deserialize_value(self, value: str) -> Self:
        assert isinstance(value, str), "Type of value is str."
        try:
            to_dict = json.loads(value)
        except:
            assert False, "The value is not converted to JSON."
        assert isinstance(to_dict, dict), "Type of convert value is Dict."

        dict_key = "check_product"
        assert isinstance(to_dict.get(dict_key), str), f"{dict_key} is not exsist dict."
        if to_dict.get(dict_key):
            dict_key = "seller_id"
            assert isinstance(
                to_dict.get(dict_key), str
            ), f"{dict_key} is not exsist dict."
            self.set_seller_id(to_dict.get(dict_key))

            dict_key = "name"
            assert isinstance(
                to_dict.get(dict_key), str
            ), f"{dict_key} is not exsist dict."
            self.set_name(to_dict.get(dict_key))

            dict_key = "description"
            assert isinstance(
                to_dict.get(dict_key), str
            ), f"{dict_key} is not exsist dict."
            self.set_description(to_dict.get(dict_key))

            dict_key = "price"
            assert isinstance(
                to_dict.get(dict_key), str
            ), f"{dict_key} is not exsist dict."
            self.set_price(int(to_dict.get(dict_key)))

        dict_key = "check_img"
        assert isinstance(to_dict.get(dict_key), str), f"{dict_key} is not exsist dict."
        if to_dict.get(dict_key):
            dict_key = "img"
            assert isinstance(
                to_dict.get(dict_key), str
            ), f"{dict_key} is not exsist dict."
            self.set_img_path(to_dict.get(dict_key))

        return self

    def set_name(self, name: str) -> Self:
        assert self.name is None, "name is already set."
        assert isinstance(name, str), "Type of name is str"

        self.name = name
        return self

    def set_description(self, description: str) -> Self:
        assert self.description is None, "rule is already set."
        assert isinstance(description, str), "Type of rule is str."

        self.description = description
        return self

    def set_price(self, price: int) -> Self:
        assert isinstance(price, int), "Type of price is int."
        assert self.price < 0, "The priceuence is already set."
        assert price >= 100, "price >= 0"

        self.price = price
        return self

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

        return self

    def set_seller_id(self, seller_id: Optional[str] = None) -> Self:
        assert self.seller_id is None, "seller id is already set."

        if seller_id is None:
            id = MemberIDBuilder().set_uuid().build()
        elif isinstance(seller_id, str):
            id = MemberIDBuilder().set_uuid(seller_id).build()
        else:
            assert False, "Type of seller_id is str."

        assert isinstance(
            seller_id, MemberID
        ), "ValueType Error: Initialize the id via MemberIDBuilder."

        self.seller_id = id
        return self

    def set_img_path(self, img_path: str) -> Result[Self, str]:
        from Commons.format import IMG_PATH
        import os.path

        assert self.img_path is None, "img path is already set."
        assert os.path.isfile(
            IMG_PATH / img_path
        ), f"Not Exsist '{str(IMG_PATH/img_path)}'. img path is not abs path."

        if not os.path.isfile(IMG_PATH / img_path):
            ic()
            print("Not Implement")
            print(f"Not Exsist '{str(IMG_PATH/img_path)}'. img path is not abs path.")
            # return Err("not exsist")

        self.img_path = img_path
        return Ok(self)

    def build(self) -> ProductTempSession:
        match (self.name, self.price, self.description, self.seller_id):
            case (None, None, None, None):
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
                img = ""
            case img if isinstance(img, str):
                img = img
            case _:
                assert False, "img path don't set."

        return ProductTempSession(
            key=self.key,
            product=product,
            img_path=img,
        )
