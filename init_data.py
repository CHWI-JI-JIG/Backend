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
        name="이호연",
        phone="0105531273",
        email="1q2w@naver.com",
        address="서울특별시 강남구 테헤란로 70",
        company_registration_number="26535793192709",
        pay_account="1495943585566122",
    ):
        case Ok(member):
            member_list.append(member)
        case a:
            assert False, f"Fail Create Member:{a}"
    match service.create(
        account="GreenGroveOrganics",
        passwd="1234",
        role="seller",
        name="Ethan Kim",
        phone="01023433123",
        email="GreenGroveOrganics@naver.com",
        address="서울특별시 강남구 테헤란로 50",
        company_registration_number="115557936219463",
        pay_account="6795943585566187",
    ):
        case Ok(member):
            member_list.append(member)
        case a:
            assert False, f"Fail Create Member:{a}"

    match service.create(
        account="yousukhair",
        passwd="1234",
        role="seller",
        name="Go Young Hee",
        phone="01013903475",
        email="yousukhair@naver.com",
        address="광주 남구 송암로 73",
        company_registration_number="114557136219462",
        pay_account="9876544925564628",
    ):
        case Ok(member):
            member_list.append(member)
        case a:
            assert False, f"Fail Create Member:{a}"

    match service.create(
        account="NatureNookMarket",
        passwd="1234",
        role="seller",
        name="Mason Lee",
        phone="01023436434",
        email="NatureNookMarket@daum.com",
        address="인천광역시 중구 차이나타운로 50",
        company_registration_number="432157136219462",
        pay_account="7952944925564628",
    ):
        case Ok(member):
            member_list.append(member)
        case a:
            assert False, f"Fail Create Member:{a}"

    match service.create(
        account="SalesSphereSeller",
        passwd="1234",
        role="seller",
        name="Park su jin",
        phone="01048372827",
        email="SalesSphereSeller@naver.com",
        address="서울특별시 강남구 영동대로 513",
        company_registration_number="48237239503827",
        pay_account="049837625673",
    ):
        case Ok(member):
            member_list.append(member)
        case a:
            assert False, f"Fail Create Member:{a}"

    match service.create(
        account="dfdf",
        passwd="123",
        role="buyer",
        name="김지희",
        phone="01052545077",
        email="dfdf@naver.com",
        address="대구광역시 수성구 달구벌대로 144",
    ):
        case Ok(member):
            member_list.append(member)
        case a:
            assert False, f"Fail Create Member:{a}"

    match service.create(
        account="snddjk234",
        passwd="1234",
        role="buyer",
        name="Lee Takgun",
        phone="01057545016",
        email="snddjk234@naver.com",
        address="대구광역시 수성구 달구벌대로 1234",
    ):
        case Ok(member):
            member_list.append(member)
        case a:
            assert False, f"Fail Create Member:{a}"

    match service.create(
        account="luckytokki",
        passwd="1234",
        role="buyer",
        name="kim su hee",
        phone="01067541234",
        email="luckytokki@daum.com",
        address="울산광역시 남구 삼산로 259",
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
        phone="01049483948",
        email="admin-chigigic@naver.com",
        address="경기도 성남시 분당구 판교역로 235",
    ):
        case Ok(member):
            member_list.append(member)
        case a:
            assert False, f"Fail Create Member:{a}"

    match service.create(
        account="happymeal",
        passwd="1234",
        role="buyer",
        name="MacDonald D Gold",
        phone="01067541234",
        email="happymeal@daum.com",
        address="광주광역시 북구 용봉로 197",
    ):
        case Ok(member):
            member_list.append(member)
        case a:
            assert False, f"Fail Create Member:{a}"

    match service.create(
        account="GroundPuppy",
        passwd="1234",
        role="buyer",
        name="Oh Hae Young",
        phone="01064344123",
        email="GroundPuppy@naver.com",
        address="서울특별시 송파구 올림픽로 240",
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
            answer=None,
            question="밥솥의 사용법을 알려주세요.",
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
            answer=None,
            question="안녕하세요. 환불 가능한가요?",
            writer_id=member_list[3],
            product_id=product_list[0],
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
            answer=None,
            question="내솥 유지보수 방법에 대해 알려주세요.",
            writer_id=member_list[2],
            product_id=product_list[1],
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
            answer="스텐 밥솥을 처음 사용하실때는, 식용유를 바른 키친타월로 닦은 후 사용 바랍니다.",
            question="스텐 주걱을 사용할 때 주의해야 할 사항이 있을까요?",
            writer_id=member_list[2],
            product_id=product_list[2],
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
            answer="평균 배송 3~4일 소요됩니다.",
            question="주방용품의 배송일은 얼마나 걸리나요?",
            writer_id=member_list[2],
            product_id=product_list[3],
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
            answer=None,
            question="안녕하세요. 환불 가능한가요?",
            writer_id=member_list[3],
            product_id=product_list[3],
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
            answer="제가 제 친구에게 선물을 한다면, 쿠쿠 IH 전기 압력밥솥 6인용을 추천드립니다.",
            question="선물하기에 좋은 밥솥이 있을까요?",
            writer_id=member_list[2],
            product_id=product_list[4],
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
            answer=None,
            question="밥솥을 사용할 때 주의할 점은 무엇인가요?",
            writer_id=member_list[2],
            product_id=product_list[5],
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
            answer="주걱, 여분패킹, 스테인리스 내솥을 추천드립니다. 고객님.",
            question="밥솥을 구매할 때 유용한 액세서리는 무엇인가요?",
            writer_id=member_list[2],
            product_id=product_list[6],
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
            answer=None,
            question="밥솥은 최대 몇 기압까지 사용 가능한가요?",
            writer_id=member_list[2],
            product_id=product_list[7],
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
            answer=None,
            question="안녕하세요. 환불 가능한가요?",
            writer_id=member_list[3],
            product_id=product_list[8],
            writer_account="",
        )
    ):
        case Ok(comment):
            comment_list.append(comment)
        case a:
            assert False, f"Fail Create Comment:{a}"

    id = CommentIDBuilder().set_uuid().set_seqence(12).build()

    match create.save_comment(
        Comment(
            id=id,
            answer="네, 파손 관련 내역은 직접 연락드리도록 하겠습니다. 감사합니다.",
            question="밥솥이 파손되어 도착했어요.",
            writer_id=member_list[2],
            product_id=product_list[8],
            writer_account="",
        )
    ):
        case Ok(comment):
            comment_list.append(comment)
        case a:
            assert False, f"Fail Create Comment:{a}"

    id = CommentIDBuilder().set_uuid().set_seqence(13).build()

    match create.save_comment(
        Comment(
            id=id,
            answer=None,
            question="밥솥을 구매할 때 가격 대비 품질이 좋은 제품은 무엇인가요?",
            writer_id=member_list[2],
            product_id=product_list[9],
            writer_account="",
        )
    ):
        case Ok(comment):
            comment_list.append(comment)
        case a:
            assert False, f"Fail Create Comment:{a}"

    id = CommentIDBuilder().set_uuid().set_seqence(14).build()

    match create.save_comment(
        Comment(
            id=id,
            answer="특수 코팅이라 내솥에 전혀 이상이 가지 않지만, 지속적으로 사용 시, 잔기스가 발생 가능합니다.",
            question="식기 세척기를 사용하면 내솥에 손상이 생길까요?",
            writer_id=member_list[2],
            product_id=product_list[10],
            writer_account="",
        )
    ):
        case Ok(comment):
            comment_list.append(comment)
        case a:
            assert False, f"Fail Create Comment:{a}"

    id = CommentIDBuilder().set_uuid().set_seqence(15).build()

    match create.save_comment(
        Comment(
            id=id,
            answer=None,
            question="안녕하세요. 환불 가능한가요?",
            writer_id=member_list[3],
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
            product_id=product_list[0],
            buyer_id=member_list[2],  # 3
            recipient_name="김지희",
            recipient_phone="01012345678",
            recipient_address="전라남도 여수시 무선로 50",
            product_name="",
            product_img_path="",
            buy_count="2",
            total_price="340000",
            order_date=datetime.now(),
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
            product_id=product_list[1],
            buyer_id=member_list[2],  # 3
            recipient_name="이지연",
            recipient_phone="01098765431",
            recipient_address="경기도 수원시 장안구 경수대로 883번길 55-3",
            product_name="",
            product_img_path="",
            buy_count="2",
            total_price="340000",
            order_date=datetime.now(),
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
            product_id=product_list[2],
            buyer_id=member_list[2],  # 3
            recipient_name="Lee Takgun",
            recipient_phone="01036574774",
            recipient_address="강원도 춘천시 명동로 31-2",
            product_name="",
            product_img_path="",
            buy_count="2",
            total_price="340000",
            order_date=datetime.now(),
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
            product_id=product_list[3],
            buyer_id=member_list[2],  # 3
            recipient_name="장예서",
            recipient_phone="01067541234",
            recipient_address="세종특별자치시 조치원읍 신안산로 32-6",
            product_name="",
            product_img_path="",
            buy_count="2",
            total_price="340000",
            order_date=datetime.now(),
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
            product_id=product_list[4],
            buyer_id=member_list[2],  # 3
            recipient_name="김효진",
            recipient_phone="01022456698",
            recipient_address="울산광역시 남구 삼산로 43번길 35",
            product_name="",
            product_img_path="",
            buy_count="2",
            total_price="340000",
            order_date=datetime.now(),
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
            product_id=product_list[5],
            buyer_id=member_list[3],  # 3
            recipient_name="류교서",
            recipient_phone="01077548965",
            recipient_address="광주광역시 서구 상무대로 1155번길 27-2",
            product_name="",
            product_img_path="",
            buy_count="2",
            total_price="340000",
            order_date=datetime.now(),
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
            product_id=product_list[6],
            buyer_id=member_list[3],  # 3
            recipient_name="Kim jihee",
            recipient_phone="01036124774",
            recipient_address="광주광역시 서구 상무대로 1155번길 27-2",
            product_name="",
            product_img_path="",
            buy_count="2",
            total_price="340000",
            order_date=datetime.now(),
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
            product_id=product_list[7],
            buyer_id=member_list[3],  # 3
            recipient_name="박종서",
            recipient_phone="01085569112",
            recipient_address="인천광역시 중구 차이나타운로 8번길 15",
            product_name="",
            product_img_path="",
            buy_count="2",
            total_price="340000",
            order_date=datetime.now(),
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
            product_id=product_list[8],
            buyer_id=member_list[3],  # 3
            recipient_name="강지호",
            recipient_phone="01047456669",
            recipient_address="부산광역시 해운대구 송정해변로 29번길 51-12",
            product_name="",
            product_img_path="",
            buy_count="2",
            total_price="340000",
            order_date=datetime.now(),
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
            product_id=product_list[9],
            buyer_id=member_list[3],  # 3
            recipient_name="강지민",
            recipient_phone="01033678823",
            recipient_address="대구광역시 수성구 달구벌대로 283길 12",
            product_name="",
            product_img_path="",
            buy_count="2",
            total_price="340000",
            order_date=datetime.now(),
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
            product_id=product_list[10],
            buyer_id=member_list[3],  # 3
            recipient_name="박주혁",
            recipient_phone="01077654432",
            recipient_address="서울특별시 강남구 테헤란로 123번길 45-6",
            product_name="",
            product_img_path="",
            buy_count="2",
            total_price="340000",
            order_date=datetime.now(),
        )
    ):
        case Ok(order):
            product_list.append(order)
        case a:
            assert False, f"Fail Create Member:{a}"