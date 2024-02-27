import __init__
from typing import List

from get_config_data import get_db_padding
from result import Result, Ok, Err
from Domains.Members import MemberID
from Domains.Products import ProductID, Product
from datetime import datetime
from icecream import ic

member_list: List[MemberID] = []
product_list: List[ProductID] = []


def init_member():
    from Migrations import MySqlCreateProduct, MySqlCreateUser
    from Applications.Members import CreateMemberService
    from Storages.Members import MySqlSaveMember

    m_m = MySqlCreateUser(get_db_padding())

    assert m_m.check_exist_user(), "Must Run --run migrate"

    service = CreateMemberService(MySqlSaveMember(get_db_padding()))
    match service.create(
        account="1q2w",
        passwd="123",
        role="seller",
        name="Lee hohun",
        phone="010566788874",
        email="vacst@naver.com",
        address="서울시 광진구",
        company_registration_number="115557936219463",
        pay_account="6795943585566187",
    ):
        case Ok(member):
            member_list.append(member)
        case a:
            assert False, f"Fail Create Member:{a}"

    match service.create(
        account="vbvb",
        passwd="12",
        role="seller",
        name="김지희",
        phone="01079143121",
        email="jihihi@daum.com",
        address="서울시 중량구",
        company_registration_number="432157136219462",
        pay_account="7952944925564628",
    ):
        case Ok(member):
            member_list.append(member)
        case a:
            assert False, f"Fail Create Member:{a}"

    match service.create(
        account="asdf",
        passwd="123",
        role="buyer",
        name="Lee Takgun",
        phone="01036574774",
        email="vacst@naver.com",
        address="서울시 구로구",
    ):
        case Ok(member):
            member_list.append(member)
        case a:
            assert False, f"Fail Create Member:{a}"

    match service.create(
        account="zxcv",
        passwd="1qq1",
        role="buyer",
        name="장예서",
        phone="01067541234",
        email="bstax@daum.com",
        address="전라북도 익산",
    ):
        case Ok(member):
            member_list.append(member)
        case a:
            assert False, f"Fail Create Member:{a}"


def init_product():
    from Storages.Products import MySqlGetProduct, MySqlSaveProduct
    from Builders.Products import ProductIDBuilder

    create = MySqlSaveProduct(get_db_padding())

    id = ProductIDBuilder().set_uuid().set_seqence(1).build()

    product = Product(
        id=id,
        seller_id=member_list[0],
        name="쿠쿠밥솥",
        img_path="img.jpg",
        price="170000",
        description="쿠쿠하세요~ 쿠쿠.",
        register_day=datetime.now(),
    )

    product_list.append(create.save_product(product))
