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
            # 커서 생성
            with connection.cursor() as cursor:
                # 판매자 ID를 기준으로 주문 목록 조회 쿼리
                select_query = f"""
SELECT
    COUNT(*) AS total_count,
    o.id,
    o.buy_count,
    b.id AS buyer_id,
    b.account AS buyer_account,
    b.phone AS buyer_phone,
    b.address AS buyer_address,
    p.id AS product_id,
    p.name AS product_name,
    p.img_path AS product_img_path,
    o.total_price,
    o.order_date
FROM
    {order_table_name} o
    JOIN {product_table_name} p ON o.product_id = p.id
    JOIN {user_table_name} b ON o.buyer_id = b.id
WHERE
    p.seller_id = %s
GROUP BY
    o.id
ORDER BY
    o.order_date DESC
LIMIT
    %s, %s;
            """
                cursor.execute(
                    select_query,
                    (
                        seller_id.get_id(),
                        page * size,  
                        size,
                    ),
                )
                
                orders_data = cursor.fetchall()
                total_count = len(orders_data)  
                orders = []
                for order_data in orders_data:
                    order = Order(
                        id=OrderIDBuilder().set_uuid(id).build(),
                        buy_count=order_data["buy_count"],
                        buyer_id=MemberID(UUID(order_data["buyer_id"])),
                        buyer_account=order_data["buyer_account"],
                        buyer_phone=order_data["buyer_phone"],
                        buyer_address=order_data["buyer_address"],
                        product_id=ProductID(UUID(order_data["product_id"])),
                        product_name=order_data["product_name"],
                        product_img_path=order_data["product_img_path"],
                        total_price=order_data["total_price"],
                        order_date=order_data["order_date"],
                    )
                    orders.append(order)
                return Ok((total_count, orders))
        except Exception as e:
            return Err(str(e))
        finally:
            connection.close()



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
        ...
    

        

        
        
        
        
        


