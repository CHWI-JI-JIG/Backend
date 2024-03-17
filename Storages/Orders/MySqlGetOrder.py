import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional, List, Tuple
from result import Result, Err, Ok
from datetime import datetime

from Domains.Products import *
from Domains.Members import *
from Domains.Orders import *
from Repositories.Orders import *
from Builders.Orders import *
from Builders.Members import *
from Builders.Products import *

from uuid import UUID

import pymysql

from icecream import ic


class MySqlGetOrder(IGetableOrder):
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

    def get_order_by_order_id(self, order_id: OrderID) -> Optional[Order]: ...

    def get_orders_by_seller_id(
        self,
        seller_id: MemberID,
        page=0,
        size=10,
    ) -> Result[Tuple[int, List[Order]], str]:
        """_summary_
        Order to look up orders with the same seller_id.

        Returns:
            Result[Tuple[int,List[Product]], str]:
                Ok( int, list ): int=> count of list max, list=> result
                Err(str): reason of Fail
        """
        connection = self.connect()
        order_table_name = self.get_padding_name("order")
        product_table_name = self.get_padding_name("product")
        user_table_name = self.get_padding_name("user")
        try:
            with connection.cursor() as cursor:
                select_query = f"""
SELECT
    o.id AS order_id,
    p.id AS product_id,
    b.id AS buyer_id,
    o.recipient_name AS recipient_name,
    o.recipient_phone AS recipient_phone,
    o.recipient_address AS recipient_address,
    p.name AS product_name,
    p.img_path AS img_path,
    o.buy_count AS buy_count,
    o.total_price AS total_price,
    o.order_date AS order_date
FROM
    {order_table_name} o
    JOIN {product_table_name} p ON o.product_id = p.id
    JOIN {user_table_name} b ON o.buyer_id = b.id
WHERE
    p.seller_id = %s
ORDER BY
    o.seq DESC
LIMIT
    %s, %s;
                """
                cursor.execute(select_query, (seller_id.get_id(), page * size, size))

                result = cursor.fetchall()
                orders = []

                for row in result:
                    (
                        order_id,
                        product_id,
                        buyer_id,
                        recipient_name,
                        recipient_phone,
                        recipient_address,
                        product_name,
                        img_path,
                        buy_count,
                        total_price,
                        order_date,
                    ) = row
                    order = Order(
                        id=OrderIDBuilder().set_uuid(order_id).build(),
                        product_id=ProductIDBuilder().set_uuid(product_id).build(),
                        buyer_id=MemberIDBuilder().set_uuid(buyer_id).build(),
                        recipient_name=recipient_name,
                        recipient_phone=recipient_phone,
                        recipient_address=recipient_address,
                        product_name=product_name,
                        product_img_path=img_path,
                        buy_count=buy_count,
                        total_price=total_price,
                        order_date=order_date,
                    )
                    orders.append(order)

                cursor.execute(
                    f"SELECT COUNT(*) FROM {order_table_name} o JOIN {product_table_name} p ON o.product_id = p.id WHERE p.seller_id = %s",
                    (seller_id.get_id(),),
                )
                total_count = cursor.fetchone()[0]

                connection.commit()

                return Ok((total_count, orders))

        except Exception as e:
            connection.close()
            return Err(str(e))

    # 구매자 주문 목록 조회
    def get_orders_by_buyer_id(
        self,
        buyer_id: MemberID,
        page=0,
        size=10,
    ) -> Result[Tuple[int, List[Order]], str]:
        """_summary_
        Get Orders with the same buyer_id.

        Returns:
            Result[Tuple[int,List[Product]], str]:
                Ok( int, list ): int=> count of list max, list=> result
                Err(str): reason of Fail
        """
        connection = self.connect()
        order_table_name = self.get_padding_name("order")
        product_table_name = self.get_padding_name("product")
        user_table_name = self.get_padding_name("user")
        try:
            with connection.cursor() as cursor:
                select_query = f"""
SELECT
    o.id AS order_id,
    p.id AS product_id,
    b.id AS buyer_id,
    o.recipient_name AS recipient_name,
    o.recipient_phone AS recipient_phone,
    o.recipient_address AS recipient_address,
    p.name AS product_name,
    p.img_path AS img_path,
    o.buy_count AS buy_count,
    o.total_price AS total_price,
    o.order_date AS order_date
FROM
    {order_table_name} o
    JOIN {product_table_name} p ON o.product_id = p.id
    JOIN {user_table_name} b ON o.buyer_id = b.id
WHERE
    o.buyer_id = %s
ORDER BY
    o.seq DESC
LIMIT
    %s, %s;
                """
                cursor.execute(select_query, (buyer_id.get_id(), page * size, size))

                result = cursor.fetchall()
                orders = []
                for row in result:
                    (
                        order_id,
                        product_id,
                        buyer_id,
                        recipient_name,
                        recipient_phone,
                        recipient_address,
                        product_name,
                        img_path,
                        buy_count,
                        total_price,
                        order_date,
                    ) = row
                    order = Order(
                        id=OrderIDBuilder().set_uuid(order_id).build(),
                        product_id=ProductIDBuilder().set_uuid(product_id).build(),
                        buyer_id=MemberIDBuilder().set_uuid(buyer_id).build(),
                        recipient_name=recipient_name,
                        recipient_phone=recipient_phone,
                        recipient_address=recipient_address,
                        product_name=product_name,
                        product_img_path=img_path,
                        buy_count=buy_count,
                        total_price=total_price,
                        order_date=order_date,
                    )
                    orders.append(order)

                cursor.execute(
                    f"SELECT COUNT(*) FROM {order_table_name} WHERE buyer_id = %s",
                    (buyer_id,),
                )
                total_count = cursor.fetchone()[0]

                connection.commit()

                return Ok((total_count, orders))

        except Exception as e:
            connection.close()
            return Err(str(e))
