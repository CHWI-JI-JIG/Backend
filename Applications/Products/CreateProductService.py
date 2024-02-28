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
        load_Product_session: ILoadableSession,
    ):
        # self.read_repo = read_member_repo
        assert issubclass(
            type(save_product), ISaveableMember
        ), "save_member_repo must be a class that inherits from ISaveableMember."

        self.product_repo = save_product

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
    ) -> Result[ProductID, str]: ...
