import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional
from result import Result, Ok, Err

from Domains.Members import *
from Domains.Products import *
from Domains.Sessions import *
from Builders.Members import *
from Repositories.Members import *
from Repositories.Products import *
from Repositories.Sessions import *

from icecream import ic


class CreateProductService:
    def __init__(
        self,
        # read_member_repo: IReadableMember,
        save_product: ISaveableProduct,
        save_product_session: ISaveableProductTempSession,
        load_session: ILoadableSession,
    ):
        assert issubclass(
            type(save_product), ISaveableMember
        ), "save_member_repo must be a class that inherits from ISaveableMember."

        self.product_repo = save_product

        assert issubclass(
            type(save_product_session), ISaveableProductTempSession
        ), "save_member_repo must be a class that inherits from ISaveableProductTempSession."

        self.save_session_repo = save_product_session

        assert issubclass(
            type(load_session), ILoadableSession
        ), "save_member_repo must be a class that inherits from ILoadableSession."

        self.load_session_repo = load_session

    def publish_temp_product_id(
        self, member_session_key: str
    ) -> Result[ProductTempSession, str]:
        # check member session
        builder = MemberSessionBuilder().set_deserialize_key(member_session_key)
        match self.load_session_repo.load_session(member_session_key):
            case Ok(json):
                match builder.set_deserialize_value(json):
                    case Ok(session):
                        user_session = session.build()
                    case _:
                        return Err("Invalid Member Session")
            case _:
                return Err("plz login")

        # publish
        product_session = ProductSessionBuilder().set_key().build()
        return self.save_session_repo.update_or_save_product_temp_session(
            product_session
        )

    def check_upload_image_path(
        self,
        img_path: str,
        product_key: str,
    ) -> Result[ProductTempSession, str]:
        # check product session
        match self.load_session_repo.load_session(product_key):
            case Ok(json):
                builder = ProductSessionBuilder().set_deserialize_key(product_key)
                match builder.set_deserialize_value(json):
                    case Ok(session):
                        product_builder = session
                    case _:
                        return Err("Invalid Product Session")
            case _:
                return Err("Not Exist Session")

        # set product Session
        match product_builder.set_img_path(img_path):
            case Ok(session):
                product = session.build()
            case _:
                return Err("Not Exist Image")

        return self.save_session_repo.update_or_save_product_temp_session(product)

    def upload_product_data(
        self,
        product_name: str,
        price: int,
        description: str,
        product_key: str,
    ) -> Result[ProductTempSession, str]:
        # check product session
        match self.load_session_repo.load_session(product_key):
            case Ok(json):
                builder = ProductSessionBuilder().set_deserialize_key(product_key)
                match builder.set_deserialize_value(json):
                    case Ok(session):
                        product_builder = session
                    case _:
                        return Err("Invalid Product Session")
            case _:
                return Err("Not Exist Session")

        # set product Session
        product = (
            product_builder.set_name(product_name)
            .set_price(price)
            .set_description(description)
            .build()
        )

        return self.save_session_repo.update_or_save_product_temp_session(product)

    def create(
        self,
        product_key: str,
    ) -> Result[ProductID, str]:
        match self.load_session_repo.load_session(product_key):
            case Ok(json):
                builder = ProductSessionBuilder().set_deserialize_key(product_key)
                match builder.set_deserialize_value(json):
                    case Ok(session):
                        product_builder = session
                    case _:
                        return Err("Invalid Product Session")
            case _:
                return Err("Not Exist Session")
