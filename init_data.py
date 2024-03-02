import __init__
from typing import List

from get_config_data import get_db_padding
from result import Result, Ok, Err
from Domains.Members import MemberID
from Domains.Products import ProductID, Product
from Domains.Comments import Comment, CommentID
from Domains.Orders import Order, OrderID
from datetime import datetime
from icecream import ic

member_list: List[MemberID] = []
product_list: List[ProductID] = []
comment_list: List[CommentID] = []
order_list: List[OrderID] = []


def init_member():
    from Migrations import MySqlCreateProduct, MySqlCreateUser
    from Applications.Members import CreateMemberService
    from Storages.Members import MySqlSaveMember

    m_m = MySqlCreateUser(get_db_padding())
    member_list.clear()

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
        account="susujin",
        passwd="123",
        role="seller",
        name="Park su jin",
        phone="01012349876",
        email="sj@naver.com",
        address="강원도 원주시",
        company_registration_number="48237239503827",
        pay_account="049837625673",
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

    match service.create(
        account="admin",
        passwd="admin",
        role="admin",
        name="관리자",
        phone="01084736475",
        email="admin@naver.com",
        address="경기도 성남시 분당구",
    ):
        case Ok(member):
            member_list.append(member)
        case a:
            assert False, f"Fail Create Member:{a}"


def init_product():
    from Storages.Products import MySqlGetProduct, MySqlSaveProduct
    from Builders.Products import ProductIDBuilder
    import init_product_data

    product_list.clear()
    create = MySqlSaveProduct(get_db_padding())

    init_product_data.init_product()


def init_comment():
    from Storages.Comments import MySqlGetComment, MySqlSaveComment
    from Builders.Comments import CommentIDBuilder
    from Domains.Comments import CommentID
    from uuid import uuid4

    comment_list.clear()
    create = MySqlSaveComment(get_db_padding())

    id = CommentIDBuilder().set_uuid().set_seqence(1).build()

    match create.save_comment(
        Comment(
            id=id,
            answer=None,  # 목아프다...춥다..아프다..
            question="요즘 어떤가요?",
            writer_id=member_list[2],
            product_id=product_list[0],
            writer_account="",
        )
    ):
        case Ok(comment):
            comment_list.append(comment)
        case a:
            assert False, f"Fail Create Comment:{a}"

    id = CommentIDBuilder().set_uuid().set_seqence(2).build()

    match create.save_comment(
        Comment(
            id=id,
            answer=None,  # 목아프다...춥다..아프다..
            question="한강 위에 고양이가 걸어갈 수 있을까요?",
            writer_id=member_list[2],
            product_id=product_list[1],
            writer_account="",
        )
    ):
        case Ok(comment):
            comment_list.append(comment)
        case a:
            assert False, f"Fail Create Comment:{a}"

    id = CommentIDBuilder().set_uuid().set_seqence(3).build()

    match create.save_comment(
        Comment(
            id=id,
            answer=None,  # 목아프다...춥다..아프다..
            question="노란 우산을 주문했는데, 노란 우비가 왔네요?",
            writer_id=member_list[2],
            product_id=product_list[2],
            writer_account="",
        )
    ):
        case Ok(comment):
            comment_list.append(comment)
        case a:
            assert False, f"Fail Create Comment:{a}"

    id = CommentIDBuilder().set_uuid().set_seqence(4).build()

    match create.save_comment(
        Comment(
            id=id,
            answer=None,  # 목아프다...춥다..아프다..
            question="그때는 맞고, 지금은 틀리다.",
            writer_id=member_list[2],
            product_id=product_list[3],
            writer_account="",
        )
    ):
        case Ok(comment):
            comment_list.append(comment)
        case a:
            assert False, f"Fail Create Comment:{a}"

    id = CommentIDBuilder().set_uuid().set_seqence(5).build()

    match create.save_comment(
        Comment(
            id=id,
            answer=None,  # 목아프다...춥다..아프다..
            question="밥은 먹고 다니냐?",
            writer_id=member_list[2],
            product_id=product_list[4],
            writer_account="",
        )
    ):
        case Ok(comment):
            comment_list.append(comment)
        case a:
            assert False, f"Fail Create Comment:{a}"

    id = CommentIDBuilder().set_uuid().set_seqence(6).build()

    match create.save_comment(
        Comment(
            id=id,
            answer=None,  # 목아프다...춥다..아프다..
            question="오잉, 나랑드, 썬칩 레츠고!",
            writer_id=member_list[2],
            product_id=product_list[5],
            writer_account="",
        )
    ):
        case Ok(comment):
            comment_list.append(comment)
        case a:
            assert False, f"Fail Create Comment:{a}"

    id = CommentIDBuilder().set_uuid().set_seqence(7).build()

    match create.save_comment(
        Comment(
            id=id,
            answer=None,  # 목아프다...춥다..아프다..
            question="지금 우리 학교는 따뜻할까요?",
            writer_id=member_list[2],
            product_id=product_list[6],
            writer_account="",
        )
    ):
        case Ok(comment):
            comment_list.append(comment)
        case a:
            assert False, f"Fail Create Comment:{a}"

    id = CommentIDBuilder().set_uuid().set_seqence(8).build()

    match create.save_comment(
        Comment(
            id=id,
            answer=None,  # 목아프다...춥다..아프다..
            question="작은 터널을 지나, 설국에 도착했을까요?",
            writer_id=member_list[2],
            product_id=product_list[7],
            writer_account="",
        )
    ):
        case Ok(comment):
            comment_list.append(comment)
        case a:
            assert False, f"Fail Create Comment:{a}"


    id = CommentIDBuilder().set_uuid().set_seqence(9).build()

    match create.save_comment(
        Comment(
            id=id,
            answer=None,  # 목아프다...춥다..아프다..
            question="안녕하세요 저는 당신의 물품을 원하지 않습니다.",
            writer_id=member_list[3],
            product_id=product_list[8],
            writer_account="",
        )
    ):
        case Ok(comment):
            comment_list.append(comment)
        case a:
            assert False, f"Fail Create Comment:{a}"

    id = CommentIDBuilder().set_uuid().set_seqence(9).build()

    match create.save_comment(
        Comment(
            id=id,
            answer=None,  # 목아프다...춥다..아프다..
            question="이웃집 토토로와 이웃집 인어공주는 어디서 살까요?",
            writer_id=member_list[2],
            product_id=product_list[8],
            writer_account="",
        )
    ):
        case Ok(comment):
            comment_list.append(comment)
        case a:
            assert False, f"Fail Create Comment:{a}"

    id = CommentIDBuilder().set_uuid().set_seqence(10).build()

    match create.save_comment(
        Comment(
            id=id,
            answer=None,  # 목아프다...춥다..아프다..
            question="고래밥, 바이러스, 기러기, 우영우, 별똥별?",
            writer_id=member_list[2],
            product_id=product_list[9],
            writer_account="",
        )
    ):
        case Ok(comment):
            comment_list.append(comment)
        case a:
            assert False, f"Fail Create Comment:{a}"

    id = CommentIDBuilder().set_uuid().set_seqence(11).build()

    match create.save_comment(
        Comment(
            id=id,
            answer=None,  # 목아프다...춥다..아프다..
            question="어데서 흰 당나귀도 오늘밤이 좋아서 응앙응앙 울을 것이다 ",
            writer_id=member_list[2],
            product_id=product_list[10],
            writer_account="",
        )
    ):
        case Ok(comment):
            comment_list.append(comment)
        case a:
            assert False, f"Fail Create Comment:{a}"
            
    
    
def init_order():
    from Storages.Orders import MySqlGetOrder, MySqlSaveOrder
    from Builders.Orders import OrderIDBuilder
    from Domains.Orders import OrderID
    from uuid import uuid4

    order_list.clear()
    create = MySqlSaveOrder(get_db_padding())
    
    id = OrderIDBuilder().set_uuid().set_seqence(1).build()
    match create.save_order(
        Order(
            id=id,
            product_id = product_list[0],
            buyer_id=member_list[2], #3
            recipient_name="김지희",
            recipient_phone="01012345678",
            recipient_address="서울시 동작구",
            product_name="",
            product_img_path="",
            buy_count = "2",
            total_price = "340000",
            order_date = datetime.now(),
            )
        ):
        case Ok(order):
            product_list.append(order)
        case a:
            assert False, f"Fail Create Member:{a}"
            
            
            
    id = OrderIDBuilder().set_uuid().set_seqence(2).build()
    match create.save_order(
        Order(
            id=id,
            product_id = product_list[1],
            buyer_id=member_list[2], #3
            recipient_name="이지연",
            recipient_phone="01098765431",
            recipient_address="서울시 광진구",
            product_name="",
            product_img_path="",
            buy_count = "2",
            total_price = "340000",
            order_date = datetime.now(),
            )
        ):
        case Ok(order):
            product_list.append(order)
        case a:
            assert False, f"Fail Create Member:{a}"
            
            
            
    id = OrderIDBuilder().set_uuid().set_seqence(3).build()
    match create.save_order(
        Order(
            id=id,
            product_id = product_list[2],
            buyer_id=member_list[2], #3
            recipient_name="Lee Takgun",
            recipient_phone="01036574774",
            recipient_address="서울시 구로구",
            product_name="",
            product_img_path="",
            buy_count = "2",
            total_price = "340000",
            order_date = datetime.now(),
            )
        ):
        case Ok(order):
            product_list.append(order)
        case a:
            assert False, f"Fail Create Member:{a}"
            
            
            
    id = OrderIDBuilder().set_uuid().set_seqence(4).build()
    match create.save_order(
        Order(
            id=id,
            product_id = product_list[3],
            buyer_id=member_list[2], #3
            recipient_name="장예서",
            recipient_phone="01067541234",
            recipient_address="전라북도 익산",
            product_name="",
            product_img_path="",
            buy_count = "2",
            total_price = "340000",
            order_date = datetime.now(),
            )
        ):
        case Ok(order):
            product_list.append(order)
        case a:
            assert False, f"Fail Create Member:{a}"
            
            
    id = OrderIDBuilder().set_uuid().set_seqence(5).build()
    match create.save_order(
        Order(
            id=id,
            product_id = product_list[4],
            buyer_id=member_list[2], #3
            recipient_name="김효진",
            recipient_phone="01022456698",
            recipient_address="서울시 은평구",
            product_name="",
            product_img_path="",
            buy_count = "2",
            total_price = "340000",
            order_date = datetime.now(),
            )
        ):
        case Ok(order):
            product_list.append(order)
        case a:
            assert False, f"Fail Create Member:{a}"
            
            
    id = OrderIDBuilder().set_uuid().set_seqence(6).build()
    match create.save_order(
        Order(
            id=id,
            product_id = product_list[5],
            buyer_id=member_list[3], #3
            recipient_name="류교서",
            recipient_phone="01077548965",
            recipient_address="서울시 용산구",
            product_name="",
            product_img_path="",
            buy_count = "2",
            total_price = "340000",
            order_date = datetime.now(),
            )
        ):
        case Ok(order):
            product_list.append(order)
        case a:
            assert False, f"Fail Create Member:{a}"
            
            
            
    id = OrderIDBuilder().set_uuid().set_seqence(7).build()
    match create.save_order(
        Order(
            id=id,
            product_id = product_list[6],
            buyer_id=member_list[3], #3
            recipient_name="Kim jihee",
            recipient_phone="01036124774",
            recipient_address="서울시 성동구",
            product_name="",
            product_img_path="",
            buy_count = "2",
            total_price = "340000",
            order_date = datetime.now(),
            )
        ):
        case Ok(order):
            product_list.append(order)
        case a:
            assert False, f"Fail Create Member:{a}"
            
            
    id = OrderIDBuilder().set_uuid().set_seqence(8).build()
    match create.save_order(
        Order(
            id=id,
            product_id = product_list[7],
            buyer_id=member_list[3], #3
            recipient_name="박종서",
            recipient_phone="01085569112",
            recipient_address="경기도 수원시",
            product_name="",
            product_img_path="",
            buy_count = "2",
            total_price = "340000",
            order_date = datetime.now(),
            )
        ):
        case Ok(order):
            product_list.append(order)
        case a:
            assert False, f"Fail Create Member:{a}"
            
            
    id = OrderIDBuilder().set_uuid().set_seqence(9).build()
    match create.save_order(
        Order(
            id=id,
            product_id = product_list[8],
            buyer_id=member_list[3], #3
            recipient_name="강지호",
            recipient_phone="01047456669",
            recipient_address="광주광역시 서구 상일로",
            product_name="",
            product_img_path="",
            buy_count = "2",
            total_price = "340000",
            order_date = datetime.now(),
            )
        ):
        case Ok(order):
            product_list.append(order)
        case a:
            assert False, f"Fail Create Member:{a}"
            
            
    id = OrderIDBuilder().set_uuid().set_seqence(10).build()
    match create.save_order(
        Order(
            id=id,
            product_id = product_list[9],
            buyer_id=member_list[3], #3
            recipient_name="강지민",
            recipient_phone="01033678823",
            recipient_address="서울시 금천구",
            product_name="",
            product_img_path="",
            buy_count = "2",
            total_price = "340000",
            order_date = datetime.now(),
            )
        ):
        case Ok(order):
            product_list.append(order)
        case a:
            assert False, f"Fail Create Member:{a}"
            
            
    id = OrderIDBuilder().set_uuid().set_seqence(11).build()
    match create.save_order(
        Order(
            id=id,
            product_id = product_list[10],
            buyer_id=member_list[3], #3
            recipient_name="박주혁",
            recipient_phone="01077654432",
            recipient_address="서울시 양천구",
            product_name="",
            product_img_path="",
            buy_count = "2",
            total_price = "340000",
            order_date = datetime.now(),
            )
        ):
        case Ok(order):
            product_list.append(order)
        case a:
            assert False, f"Fail Create Member:{a}"