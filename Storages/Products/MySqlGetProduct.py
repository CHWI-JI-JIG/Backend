import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional, List, Tuple
from result import Result, Err, Ok
from datetime import datetime

from Domains.Products import *
from Domains.Members import *
from Repositories.Products import *
from Builders.Products import *
from Builders.Members import *

import pymysql

from icecream import ic


class MySqlGetProduct(IGetableProduct):
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
            client_flag=pymysql.constants.CLIENT.MULTI_STATEMENTS,
        )

    def get_padding_name(self, name: str) -> str:
        return f"{self.name_padding}{name}"

    # 상품 상세페이지
    def get_product_by_product_id(self, product_id: ProductID) -> Optional[Product]:
        connection = self.connect()
        product_table_name = self.get_padding_name("product")
        try:
            with connection.cursor() as cursor:
                query = f"""
SELECT id, seller_id, name, img_path, price, description, register_day
FROM {product_table_name}
WHERE id = %s
"""
                cursor.execute(query, (product_id.get_id(),))
                result = cursor.fetchone()

                if result is None:
                    return None

                id, seller_id, name, img_path, price, description, register_day = result

                match (
                    MemberIDBuilder()
                    .set_uuid(seller_id)
                    .map(lambda b:b.build())
                ):
                    case Ok(mid):
                        product = Product(
                            id=product_id,
                            seller_id=mid,
                            name=name,
                            img_path=img_path,
                            price=price,
                            description=description,
                            register_day=register_day,
                        )
                    case e:
                        ic()
                        ic(e)
                        return None

                connection.commit()

                return product

        except Exception as e:
            print(e)
            connection.close()
            return None

    # 메인 페이지
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

        connection = self.connect()
        product_table_name = self.get_padding_name("product")
        try:
            with connection.cursor() as cursor:
                offset = page * size
                query = f"""
SELECT id, seller_id, name, img_path, price, description, register_day
FROM {product_table_name}
ORDER BY seq DESC
LIMIT %s, %s
"""
                cursor.execute(query, (offset, size))
                result = cursor.fetchall()

                products = []
                for row in result:
                    id, seller_id, name, img_path, price, description, register_day = (
                        row
                    )
                    match (
                        ProductIDBuilder().set_uuid(id).map(lambda b: b.build()),
                        MemberIDBuilder().set_uuid(seller_id).map(lambda b: b.build()),
                    ):
                        case Ok(pid), Ok(mid):
                            product = Product(
                                id=pid,
                                seller_id=mid,
                                name=name,
                                img_path=img_path,
                                price=price,
                                description=description,
                                register_day=register_day,
                            )
                            products.append(product)
                        case p, m:
                            ic()
                            ic(p, m)
                            assert False, f"p:{p} \ m:{m}"

                cursor.execute(f"SELECT COUNT(*) FROM {product_table_name}")
                total_count = cursor.fetchone()[0]

                connection.commit()

                return Ok((total_count, products))

        except Exception as e:
            print(e)
            connection.close()
            return Err(str(e))

    # 판매자 페이지
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
        connection = self.connect()
        product_table_name = self.get_padding_name("product")
        try:
            with connection.cursor() as cursor:
                offset = page * size
                query = f"""
SELECT seq,id, seller_id, name, img_path, price, description, register_day
FROM {product_table_name}
WHERE seller_id = %s
ORDER BY register_day DESC
LIMIT %s, %s
"""
                cursor.execute(query, (seller_id.get_id(), offset, size))
                result = cursor.fetchall()

                products = []
                for row in result:
                    seq, id, _, name, img_path, price, description, register_day = row
                    match (
                        ProductIDBuilder()
                        .set_seqence(seq)
                        .set_uuid(id)
                        .map(lambda b:b.build())
                    ):
                        case Ok(pid):
                            product = Product(
                                id=pid,
                                seller_id=seller_id,
                                name=name,
                                img_path=img_path,
                                price=price,
                                description=description,
                                register_day=register_day,
                            )
                            products.append(product)
                        case p:
                            ic()
                            ic(p)
                            assert False, "Not Convert ID"

                cursor.execute(
                    f"SELECT COUNT(*) FROM {product_table_name} WHERE seller_id = %s",
                    (seller_id.get_id(),),
                )
                total_count = cursor.fetchone()[0]

                connection.commit()

                return Ok((total_count, products))

        except Exception as e:
            print(e)
            connection.close()
            return Err(str(e))
