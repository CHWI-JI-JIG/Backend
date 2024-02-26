import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional
from result import Result, Err, Ok

from Domains.Products import *
from Repositories.Products import *
from uuid import UUID

import pymysql

from icecream import ic


class MySqlSaveProduct(ISaveableProduct):
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

    def save_product(self, product: Product) -> Result[ProductID, str]:
        connection = self.connect()
        product_table_name = self.get_padding_name("product")
        product.id.get_id()
        try:
            # 커서 생성
            with connection.cursor() as cursor:
                insert_query = f"""
INSERT INTO {product_table_name} (
    id,
    name,
    img_path,
    price,
    description,
    register_day
) VALUES (%s, %s, %s, %s, %s, %s);
                """
                cursor.execute(
                    insert_query,
                    (
                        product.id.get_id(),
                        product.name,
                        product.img_path,
                        product.price,
                        product.description,
                        product.register_day,
                    ),
                )
                # 변경 사항을 커밋
                connection.commit()
                return Ok(product.id.uuid)
        except Exception as e:
            connection.rollback()
            connection.close()
            return Err(str(e))
