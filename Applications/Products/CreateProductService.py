import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional
from result import Result, Ok, Err

from Domains.Members import *
from Domains.Products import *
from Domains.Sessions import *
from Builders.Members import *
from Repositories.Members import *

from icecream import ic


class CreateProductService:
    def __init__(
        self,
        # read_member_repo: IReadableMember,
        save_member_repo: ISaveableMember,
    ):
        # self.read_repo = read_member_repo
        assert issubclass(
            type(save_member_repo), ISaveableMember
        ), "save_member_repo must be a class that inherits from ISaveableMember."

        self.save_repo = save_member_repo

    def publish_temp_product_id(
        self, member_session_key: str
    ) -> Result[ProductTempSession, str]: ...

    def check_upload_image_path(
        self,
        img_path: str,
        product_key: str,
    ) -> Result[ProductTempSession, str]: ...

    def upload_product_data(
        self,
        product_name: str,
        price: int,
        description: str,
        product_key: str,
    ) -> Result[ProductTempSession, str]: ...

    def create(
        self,
        product_key: str,
    ) -> Result[ProductID, str]:
        from uuid import uuid4

        return Ok(ProductID(uuid=uuid4(), sequence=1))

        return Err("11")
