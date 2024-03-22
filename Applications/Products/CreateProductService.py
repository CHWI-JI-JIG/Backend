import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional
from result import Result, Ok, Err

from Domains.Members import *
from Domains.Products import *
from Domains.Sessions import *
from Builders.Members import *
from Builders.Products import *
from Repositories.Members import *
from Repositories.Products import *
from Repositories.Sessions import *

from datetime import datetime
from icecream import ic


class CreateProductService:
    def __init__(
        self,
        # read_member_repo: IReadableMember,
        save_product: ISaveableProduct,
        save_product_session: IUptadeORSaveProductTempSession,
        load_session: ILoadableSession,
    ):

        assert issubclass(
            type(save_product), ISaveableProduct
        ), "save_member_repo must be a class that inherits from  ISaveableProduct."

        self.product_repo = save_product

        assert issubclass(
            type(save_product_session), IUptadeORSaveProductTempSession
        ), "save_member_repo must be a class that inherits from  IUptadeORSaveProductTempSession."

        self.save_session_repo = save_product_session

        assert issubclass(
            type(load_session), ILoadableSession
        ), "save_member_repo must be a class that inherits from ILoadableSession."

        self.load_session_repo = load_session

    def publish_temp_product_id(
        self, user_session_key: str
    ) -> Result[ProductTempSession, str]:
        # check member session
        builder = MemberSessionBuilder().set_deserialize_key(user_session_key)
        match self.load_session_repo.load_session(user_session_key):
            case Ok(json):
                match builder.set_deserialize_value(json):
                    case Ok(session):
                        user_session = session.build()
                        if user_session.role != RoleType.SELLER:
                            return Err("Permission Deny")
                    case _:
                        return Err("Invalid Member Session")
            case _:
                return Err("plz login")

        # publish
        match (
            ProductSessionBuilder()
            .set_key()
            .unwrap()  # 오류가 생길 확률이 없으므로 unwrap
            .set_use_count()
            .set_create_time()
            .set_owner_id(user_session.owner_id)
            .unwrap() # 오류가 생길 확률이 없으므로 unwrap
            .set_seller_id(user_session.member_id.get_id())
            .map(lambda b: b.build())
        ):
            case Ok(Ok(product_session)):
                return self.save_session_repo.update_or_save_product_temp_session(
                    product_session
                )
            case e:
                print(e)
                return e

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
                    case e:
                        ic(e)
                        return Err("Invalid Product Session")
            case _:
                return Err("Not Exist Session")

        # set product Session
        match product_builder.set_img_path(img_path).map(lambda b: b.build()):
            case Ok(Ok(session)):
                product = session
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
        match (
            product_builder.set_name(product_name)
            .set_price(price)
            .set_description(description)
            .build()
        ):
            case Ok(product):
                return self.save_session_repo.update_or_save_product_temp_session(
                    product
                )
            case e:
                return e

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

        if not (
            product_builder.check_set_img() and product_builder.check_set_product()
        ):
            return Err("Not Set Data")
        match product_builder.build():
            case Ok(product):
                img_path = product.img_path
                seller_id = product.seller_id
                product = product.product
            case e:
                return e

        id = ProductIDBuilder().set_uuid().unwrap().build()

        return self.product_repo.save_product(
            Product(
                id=id,
                seller_id=seller_id,
                name=product.name,
                img_path=img_path,
                price=product.price,
                description=product.description,
                register_day=datetime.now(),
            )
        )
