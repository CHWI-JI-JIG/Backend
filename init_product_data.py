import __init__
from typing import List
import csv
import os
from get_config_data import get_db_padding
from result import Result, Ok, Err
from Domains.Members import MemberID
from Domains.Products import ProductID, Product
from Domains.Comments import Comment, CommentID
from datetime import datetime
from icecream import ic
import random

def init_product():
    from Storages.Products import MySqlGetProduct, MySqlSaveProduct
    from Builders.Products import ProductIDBuilder
    from init_data import member_list, product_list

    product_list.clear()
    create = MySqlSaveProduct(get_db_padding())

    id = ProductIDBuilder().set_uuid().set_seqence(1).build()

    # CSV 파일 경로
    csv_path = "docs/init_product_list.csv"

    with open(csv_path, "r", encoding="utf-8") as csvfile:
        csvreader = csv.DictReader(csvfile)

        for row in csvreader:
            id = ProductIDBuilder().set_uuid().set_seqence(1).build()
            
            random_seller_index = random.randint(0, 2)
            seller_member = member_list[random_seller_index]

            match create.save_product(
                Product(
                    id=id,
                    seller_id=seller_member,
                    name=row["상품 이름"],
                    img_path=row["상품 이미지"],
                    price=str(row["상품 가격"]),
                    description=row["상품 설명"],
                    register_day=datetime.now(),
                )
            ):
                case Ok(product):
                    product_list.append(product)
                case a:
                    assert False, f"Fail Create Member:{a}"
