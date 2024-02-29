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

        self.load_repo = load_session

    def publish_temp_product_id(
        self, member_session_key: str
    ) -> Result[ProductTempSession, str]:
        # check member session
        match self.load_repo.load_session(member_session_key):
            case Ok(json):
                user_session = (
                    MemberSessionBuilder()
                    .set_deserialize_key(member_session_key)
                    .set_deserialize_value(json)
                    .unwrap()
                    .build()
                )
            case _:
                return Err("plz login")

        # publish

    def check_upload_image_path(
        self,
        img_path: str,
        product_key: str,
    ) -> Result[ProductTempSession, str]:
        from uuid import uuid4
        IMG_PATH = __init__.root_path/"Images"
        import os
        
        product_id = ProductID(uuid=uuid4(), sequence=1)
        seller_id = MemberID(uuid=uuid4(), sequence=1)
        product = Product(id=product_id, seller_id=seller_id)
        key = uuid4() 
        img_path = IMG_PATH
        
        ic(ProductTempSession(key, product, img_path))
        return Ok(ProductTempSession(key, product, img_path))
            
        return Err("11")

    def upload_product_data(
        self,
        product_name: str,
        price: int,
        description: str,
        product_key: str,
    ) -> Result[ProductTempSession, str]:
        from uuid import uuid4
        IMG_PATH = __init__.root_path/"Images"
        import os
        from icecream import ic
        
        product_id = ProductID(uuid=uuid4(), sequence=1)
        seller_id = MemberID(uuid=uuid4(), sequence=1)
        product = Product(id=product_id, seller_id=seller_id, name='쿠첸밥솥', price=2000000, description='쿠첸하세요~ 쿠첸.')
        key = uuid4() 
        
        return Ok(ProductTempSession(key, product))
        return Err("11")

    def create(
        self,
        product_key: str,
    ) -> Result[ProductID, str]:
        from uuid import uuid4

        return Ok(ProductID(uuid=uuid4(), sequence=1))

        return Err("11")
