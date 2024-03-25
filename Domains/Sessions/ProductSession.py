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
from Domains.Sessions import (
    ISessionSerializeable,
    ISessionBuilder,
    SecuritySession,
    SecuritySessionBuilder,
    SessionToken,
)
from Domains import ID
from Domains.Members import *
from Builders.Members import *
from Builders.Products import *
from Domains.Products import *

from icecream import ic


@dataclass(frozen=True)
class ProductTempSession(ID, ISessionSerializeable, SecuritySession):
    key: UUID
    seller_id: MemberID
    product: Optional[Product]
    img_path: str = ""

    max_count:int = 7
    minute:int=20
    
    def MAX_USE_COUNT(self) -> int:
        return self.max_count
    def VALIDE_MINUTE(self) -> int:
        return self.minute
    def get_id(self) -> str:
        return self.key.hex

    def serialize_key(self) -> str:
        return self.get_id()

    def serialize_value(self) -> str:
        match (self.product, self.img_path):
            case (p, i) if isinstance(p, Product) and len(i) > 0:
                return json.dumps(
                    {
                        "check_product": True,
                        "check_img": True,
                        "seller_id": self.seller_id.get_id(),
                        "name": p.name,
                        "price": p.price,
                        "description": p.description,
                        "img_path": i,
                    },
                    ensure_ascii=False,
                )

            case (none, i) if len(i) > 0 and none is None:
                return json.dumps(
                    {
                        "check_product": False,
                        "check_img": True,
                        "seller_id": self.seller_id.get_id(),
                        "img_path": i,
                    },
                    ensure_ascii=False,
                )
            case (p, none) if len(none) <= 0 and isinstance(p, Product):
                return json.dumps(
                    {
                        "check_product": True,
                        "check_img": False,
                        "seller_id": self.seller_id.get_id(),
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
                        "seller_id": self.seller_id.get_id(),
                    },
                    ensure_ascii=False,
                )


class ProductSessionBuilder(ISessionBuilder, SecuritySessionBuilder):
    def __init__(
        self,
        key: Optional[UUID] = None,
        name: Optional[str] = None,
        price: Optional[int] = None,
        description: Optional[str] = None,
        img_path: Optional[str] = None,
    ):
        super().__init__(key=key)
        self.key = key
        self.seller_id: Optional[MemberID] = None
        self.name: Optional[name] = name
        self.price = price
        self.description = description
        self.img_path = img_path

    def check_set_img(self) -> bool:
        return isinstance(self.img_path, str)

    def check_set_product(self) -> bool:

        return (
            isinstance(self.seller_id, MemberID)
            and isinstance(self.name, str)
            and isinstance(self.price, int)
            and isinstance(self.description, str)
        )

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

        dict_key = "seller_id"
        if not isinstance(to_dict.get(dict_key), str):
            return Err(f"Not Exists {dict_key}")
        self.set_seller_id(to_dict.get(dict_key))

        dict_key = "check_product"
        if not isinstance(to_dict.get(dict_key), bool):
            return Err(f"Not Exists {dict_key}")
        if to_dict.get(dict_key):
            dict_key = "name"
            if not isinstance(to_dict.get(dict_key), str):
                return Err(f"Not Exists {dict_key}")
            self.set_name(to_dict.get(dict_key))

            dict_key = "description"
            if not isinstance(to_dict.get(dict_key), str):
                return Err(f"Not Exists {dict_key}")
            self.set_description(to_dict.get(dict_key))

            dict_key = "price"
            if not isinstance(to_dict.get(dict_key), int):
                return Err(f"Not Exists {dict_key}")
            self.set_price(int(to_dict.get(dict_key)))

        dict_key = "check_img"
        if not isinstance(to_dict.get(dict_key), bool):
            return Err(f"Not Exists {dict_key}")
        if to_dict.get(dict_key):
            dict_key = "img_path"
            if not isinstance(to_dict.get(dict_key), str):
                return Err(f"Not Exists {dict_key}")
            self.set_img_path(to_dict.get(dict_key))

        return (
            self.set_use_count(token.use_count)
            .set_create_time(token.create_time)
            .set_owner_id(token.owner_id)
        )

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
        assert self.price is None, "The priceuence is already set."
        assert price >= 100, "price >= 0"

        self.price = price
        return self

    def set_seller_id(self, seller_id: str) -> Result[Self, str]:
        assert self.seller_id is None, "seller id is already set."

        if isinstance(seller_id, str):
            match MemberIDBuilder().set_uuid(seller_id).map(lambda b: b.build()):
                case Ok(ret):
                    id = ret
                case e:
                    return e
        else:
            assert False, "Type of seller_id is str."
            return Err("Type of seller_id is str.")

        assert isinstance(
            id, MemberID
        ), "ValueType Error: Initialize the id via MemberIDBuilder."

        self.seller_id = id
        return Ok(self)

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

    def build(self) -> Result[ProductTempSession, str]:
        assert isinstance(self.seller_id, MemberID), "Not Set seller_id"
        self.assert_and_check_about_setting()

        match (self.name, self.price, self.description, self.seller_id):
            case (None, None, None, _):
                product = None
            case (name, price, description, seller_id) if (
                isinstance(name, str)
                and isinstance(price, int)
                and isinstance(description, str)
                and isinstance(seller_id, MemberID)
            ):
                match ProductIDBuilder().set_uuid().map(lambda b: b.build()):
                    case Ok(id):
                        product = Product(
                            id=id,
                            seller_id=seller_id,
                            name=name,
                            description=description,
                            img_path="Dump",
                            register_day=datetime.now(),
                            price=price,
                        )
                    case e:
                        return e
            case _:
                assert False, "Not Set name, price, description, seller_id."
                return Err("Not Set name, price, description, seller_id.")

        match self.img_path:
            case None:
                img_path = ""
            case img_path if isinstance(img_path, str):
                img_path = img_path
            case _:
                assert False, "img path don't set."
                return Err("img path don't set.")

        return Ok(
            ProductTempSession(
                key=self.key,
                seller_id=self.seller_id,
                product=product,
                img_path=img_path,
                owner_id=self.owner_id,
                create_time=self.create_time,
                use_count=self.use_count,
            )
        )
