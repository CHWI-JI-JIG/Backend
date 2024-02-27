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

    match create.save_product(Product(
        id=id,
        seller_id=member_list[0],
        name="쿠쿠밥솥",
        img_path="img.jpg",
        price="170000",
        description="쿠쿠하세요~ 쿠쿠.",
        register_day=datetime.now(),
    )):
        case Ok(product):
            product_list.append(product)
        case a:
            assert False, f"Fail Create Member:{a}"

    id = ProductIDBuilder().set_uuid().set_seqence(2).build()
    match create.save_product(Product(
        id=id,
        seller_id=member_list[1],
        name="전기밥솥",
        img_path="/path/to/image1.jpg",
        price="8768",
        description="이 밥솥은 효율적이고 간편한 밥을 만들어냅니다. 최고의 맛과 건강을 위해 지금 주문하세요!",
        register_day=datetime.now(),
    )):
        case Ok(product):
            product_list.append(product)
        case a:
            assert False, f"Fail Create Member:{a}"

    id = ProductIDBuilder().set_uuid().set_seqence(3).build()
    match create.save_product(Product(
        id=id,
        seller_id=member_list[0],
        name="식기세트",
        img_path="/path/to/image2.jpg",
        price="3567",
        description= "이 식기세트로 특별한 식사를 즐겨보세요. 심플하고 우아한 디자인으로 가정의 테이블을 더 아름답게 만들어줍니다.",
        register_day=datetime.now(),
    )):
        case Ok(product):
            product_list.append(product)
        case a:
            assert False, f"Fail Create Member:{a}"         

    id = ProductIDBuilder().set_uuid().set_seqence(4).build()
    match create.save_product(Product(
        id=id,
        seller_id=member_list[1],
        name="전기포트",
        img_path="/path/to/image3.jpg",
        price="5483",
        description= "강력한 가열 성능과 스타일리시한 디자인으로 이 전기포트는 여러분의 생활을 편리하게 해줍니다. 물을 끓이는 것을 더 즐겁게 만들어줍니다!",
        register_day=datetime.now(),
    )):
        case Ok(product):
            product_list.append(product)
        case a:
            assert False, f"Fail Create Member:{a}"  

    id = ProductIDBuilder().set_uuid().set_seqence(5).build()
    match create.save_product(Product(
        id=id,
        seller_id=member_list[1],
        name="식기건조대",
        img_path="/path/to/image.5jpg",
        price="9217",
        description= "이 식기건조대는 깨끗하고 정리된 주방을 만들어줍니다. 효율적인 공간 활용과 환기 시스템으로 식기를 완벽하게 건조시켜줍니다!",
        register_day=datetime.now(),
    )):
        case Ok(product):
            product_list.append(product)
        case a:
            assert False, f"Fail Create Member:{a}"              

    id = ProductIDBuilder().set_uuid().set_seqence(6).build()
    match create.save_product(Product(
        id=id,
        seller_id=member_list[0],
        name="숟가락",
        img_path="/path/to/image6.jpg",
        price="2094",
        description= "이 숟가락은 튼튼하고 편안한 그립감으로 여러분의 식사를 더욱 편리하게 만들어줍니다. 식기 세트에 꼭 필요한 아이템입니다!",
        register_day=datetime.now(),
    )):
        case Ok(product):
            product_list.append(product)
        case a:
            assert False, f"Fail Create Member:{a}" 

    id = ProductIDBuilder().set_uuid().set_seqence(7).build()
    match create.save_product(Product(
        id=id,
        seller_id=member_list[0],
        name="컵",
        img_path="/path/to/image7.jpg",
        price="3121",
        description= "이 컵은 환경을 생각한 친환경적인 디자인으로 제작되었습니다. 건강하고 안전한 식습관을 위해 지금 사용하세요!",
        register_day=datetime.now(),
    )):
        case Ok(product):
            product_list.append(product)
        case a:
            assert False, f"Fail Create Member:{a}" 

    id = ProductIDBuilder().set_uuid().set_seqence(8).build()
    match create.save_product(Product(
        id=id,
        seller_id=member_list[0],
        name="식탁",
        img_path="/path/to/image8.jpg",
        price="6054",
        description= "이 식탁은 가정의 모임을 더욱 특별하게 만들어줍니다. 품질과 편안함을 동시에 제공하는 최고의 선택입니다!",
        register_day=datetime.now(),
    )):
        case Ok(product):
            product_list.append(product)
        case a:
            assert False, f"Fail Create Member:{a}" 

    id = ProductIDBuilder().set_uuid().set_seqence(9).build()
    match create.save_product(Product(
        id=id,
        seller_id=member_list[1],
        name="밥공기",
        img_path="/path/to/image9.jpg",
        price="6028",
        description= "이 밥공기는 내용물을 따뜻하게 보관해줍니다. 더 나은 식사 경험을 위해 바로 사용하세요!",
        register_day=datetime.now(),
    )):
        case Ok(product):
            product_list.append(product)
        case a:
            assert False, f"Fail Create Member:{a}"             

    id = ProductIDBuilder().set_uuid().set_seqence(10).build()
    match create.save_product(Product(
        id=id,
        seller_id=member_list[0],
        name="식기건조기",
        img_path="/path/to/image10.jpg",
        price="9531",
        description= "이 식기건조기는 효율적이고 안전한 방식으로 식기를 건조시켜줍니다. 깨끗하고 청결한 주방을 위해 선택하세요!",
        register_day=datetime.now(),
    )):
        case Ok(product):
            product_list.append(product)
        case a:
            assert False, f"Fail Create Member:{a}"  

    id = ProductIDBuilder().set_uuid().set_seqence(11).build()
    match create.save_product(Product(
        id=id,
        seller_id=member_list[1],
        name="오븐",
        img_path="/path/to/image11.jpg",
        price="9531",
        description= "이 오븐은 효율적이고 안전한 방식으로 음식을 구워줍니다.",
        register_day=datetime.now(),
    )):
        case Ok(product):
            product_list.append(product)
        case a:
            assert False, f"Fail Create Member:{a}"  

    id = ProductIDBuilder().set_uuid().set_seqence(12).build()
    match create.save_product(Product(
        id=id,
        seller_id=member_list[0],
        name="포크",
        img_path="/path/to/image12.jpg",
        price="9531",
        description= "이 포크는 사용성이 아주 좋습니다.",
        register_day=datetime.now(),
    )):
        case Ok(product):
            product_list.append(product)
        case a:
            assert False, f"Fail Create Member:{a}"              