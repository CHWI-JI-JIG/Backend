import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional, List, Tuple
from result import Result, Err, Ok
from datetime import datetime

from Domains.Products import *
from Domains.Members import *
from Repositories.Products import *
from Builders.Products import *

import pymysql

# from icecream import ic


class GetableProduct(IGetableProduct):
    def __init__(self, name_padding: str = "log_"):
        self.name_padding = name_padding

    def connect(self):
        from get_config_data import get_mysql_dict

        sql_config = get_mysql_dict()
        return pymysql.connect(
            host=sql_config["host"],
            user=sql_config["user"],
            password=sql_config["password"],
            db=sql_config["database"],
            charset=sql_config["charset"],
        )

    def get_padding_name(self, name: str) -> str:
        return f"{self.name_padding}{name}"
    
    
    ##
    def get_product_by_product_id(self, product_id: ProductID) -> Optional[Product]: ...
    
    
    ##
    def get_products_by_create_date(
        self,
        page=0,
        size=10,
    ) -> Result[Tuple[int, List[Product]], str]:
        """_summary_

        Args:
            page (int, optional): _description_. Defaults to 0.
            size (int, optional): _description_. Defaults to 10.

        Returns:
            Result[Tuple[int,List[Product]], str]:
                Ok( int, list ): int=> count of list max, list=> result
                Err(str): reason of Fail
        """
        ...
        
        
    ##    
    def get_products_by_seller_id(
        self,
        seller_id: MemberID,
        page=0,
        size=10,
    ) -> Result[Tuple[int, List[Product]], str]:
        """_summary_
        Product to look up Products with the same seller_id.

        Returns:
            Result[Tuple[int,List[Product]], str]:
                Ok( int, list ): int=> count of list max, list=> result
                Err(str): reason of Fail
        """
        ...
        
        
        
        
        


