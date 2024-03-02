import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional
from result import Result, Err, Ok

from Domains.Orders import *
from Repositories.Orders import *
from uuid import UUID

import pymysql

from icecream import ic


class MySqlSaveOrder(ISaveableOrder):
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

    def save_order(self, order: Order) -> Result[OrderID, str]:
        connection = self.connect()
        order_table_name = self.get_padding_name("order")
        try:
            # 커서 생성
            with connection.cursor() as cursor:
                insert_query = f"""
INSERT INTO {order_table_name} (
    id,
    product_id,
    buyer_id,
    recipient_name,
    recipient_phone,
    recipient_address,
    buy_count,
    total_price,
    order_date
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
                cursor.execute(
                    insert_query,
                    (
                        order.id.get_id(),
                        order.product_id.get_id(),
                        order.buyer_id.get_id(),
                        order.recipient_name,
                        order.recipient_phone,
                        order.recipient_address,
                        order.buy_count,
                        order.total_price,
                        order.order_date,
                    ),
                )
                # 변경 사항을 커밋
                connection.commit()
                return Ok(order.id)
        except Exception as e:
            connection.rollback()
            connection.close()
            return Err(str(e))
