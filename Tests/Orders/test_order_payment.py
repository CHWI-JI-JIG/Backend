import __init__
import unittest
import sys

from typing import List
from result import Result, Ok, Err
import copy

from Migrations import *

from Domains.Members import *
from Domains.Products import *
from Domains.Orders import *
from Domains.Sessions import *

from Builders.Members import *
from Builders.Products import *

from Applications.Members.ExtentionMethod import hashing_passwd
from Applications.Members import *
from Applications.Products import *
from Applications.Orders import *
from Applications.Payments import PayData, PaymentService, PandasCsvPaymentStorage

from Storages.Members import *
from Storages.Products import *
from Storages.Orders import *
from Storages.Sessions import *


from get_config_data import get_db_padding, set_db_padding
from init_data import (
    member_list,
    product_list,
    init_member,
    init_product,
    init_order,
)

from icecream import ic


class test_order_builder(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = "test"
        print(sys._getframe(0).f_code.co_name, f"(test_order_builder)")
        set_db_padding("test_order_service_")

        mm = MySqlCreateUser(get_db_padding())
        cls.user_migrate = mm
        mp = MySqlCreateProduct(get_db_padding())
        cls.product_migrate = mp
        mo = MySqlCreateOrder(get_db_padding())
        cls.order_migrate = mo
        ms = MySqlCreateSession(get_db_padding())
        cls.session_migrate = ms

        cls.pay_service = PaymentService()
        cls.csv_path = cls.pay_service.pay_repo.file_path

        if ms.check_exist_session():
            ms.delete_session()
        if mo.check_exist_order():
            mo.delete_order()
        if mp.check_exist_product():
            mp.delete_product()
        if mm.check_exist_user():
            mm.delete_user()

        load_storage = MySqlLoadSession(get_db_padding())
        get_product = MySqlGetProduct(get_db_padding())
        service = CreateMemberService(MySqlSaveMember(get_db_padding()))
        cls.member_create_service = service

        login = AuthenticationMemberService(
            auth_member_repo=MySqlLoginAuthentication(get_db_padding()),
            session_repo=MySqlMakeSaveMemberSession(get_db_padding()),
            load_repo=MySqlLoadSession(get_db_padding()),
            del_session_repo=MySqlDeleteSession(get_db_padding()),
        )
        cls.login_service = login

        service = ReadProductService(
            get_product_repo=MySqlGetProduct(get_db_padding()),
            load_session_repo=load_storage,
        )
        cls.product_read_service = service
        service = CreateProductService(
            save_product=MySqlSaveProduct(get_db_padding()),
            save_product_session=MySqlSaveProductTempSession(get_db_padding()),
            load_session=load_storage,
        )
        cls.product_create_service = service

        service = AuthenticationMemberService(
            auth_member_repo=MySqlLoginAuthentication(get_db_padding()),
            session_repo=MySqlMakeSaveMemberSession(get_db_padding()),
            load_repo=MySqlLoadSession(get_db_padding()),
            del_session_repo=MySqlDeleteSession(get_db_padding()),
        )
        cls.login_service = service

        service = ReadOrderService(
            get_order_repo=MySqlGetOrder(get_db_padding()),
            load_session_repo=load_storage,
        )
        cls.read_order_service = service

        service = ReadProductService(
            get_product_repo=get_product,
            load_session_repo=load_storage,
        )
        cls.read_product_service = service

        service = OrderPaymentService(
            save_order=MySqlSaveOrder(get_db_padding()),
            save_transition=MySqlSaveOrderTransition(get_db_padding()),
            load_session=load_storage,
            get_product=get_product,
        )
        cls.order_and_payment_service = service

        mm.create_user()
        init_member()
        mp.create_product()
        init_product()
        ms.create_session()

    @classmethod
    def tearDownClass(cls):
        "Hook method for deconstructing the class fixture after running all tests in the class."
        print(sys._getframe(0).f_code.co_name)
        mm = cls.user_migrate
        mp = cls.product_migrate
        mo = cls.order_migrate
        ms = cls.session_migrate
        if ms.check_exist_session():
            ms.delete_session()
        if mo.check_exist_order():
            mo.delete_order()
        if mp.check_exist_product():
            mp.delete_product()
        if mm.check_exist_user():
            mm.delete_user()

    def setUp(self):
        "Hook method for setting up the test fixture before exercising it."
        print("\t", sys._getframe(0).f_code.co_name)
        self.order_migrate.create_order()
        init_order()

    def tearDown(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t", sys._getframe(0).f_code.co_name)
        if self.order_migrate.check_exist_order():
            self.order_migrate.delete_order()

    def test_pay_service(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t\t", sys._getframe(0).f_code.co_name)

        match self.pay_service.approval_and_logging(
            transition_key="aaa",
            total_price=10000,
            card_account="1111-1111-1111-1111",
        ):
            case Ok(success):
                assert success, "Error"
            case e:
                assert False, f"{e}"

        match self.pay_service.approval_and_logging(
            transition_key="aaa",
            total_price=100000000,
            card_account="1111-1111-1111-1111",
        ):
            case Err("Insufficient funds in the card"):
                pass
            case e:
                assert False, f"{e}"

        match self.pay_service.approval_and_logging(
            transition_key="aaa",
            total_price=300000,
            card_account="2222-2222-2222-2222",
        ):
            case Ok(success):
                assert success, "Error"
            case e:
                assert False, f"{e}"

        match self.pay_service.approval_and_logging(
            transition_key="aaa",
            total_price=300000,
            card_account="2223-2222-2222-2222",
        ):
            case Err("Invalid card number"):
                pass
            case e:
                assert False, f"{e}"

    def test_회원생성_주문조회_상품조회및선택_트렌젝션생성_결제완료_주문조회(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t\t", sys._getframe(0).f_code.co_name)
        # 회원 생성
        match self.member_create_service.create(
            account="qawsars",
            passwd="123",
            role="buyer",
            name="lee Tak",
            phone="01023459087",
            email="arst@daum.com",
            address="guri",
        ):
            case Ok(member_id):
                mid = member_id
            case _:
                assert False, "Fail Create Member"
        # login
        match self.login_service.login("qawsars", "134"):
            case Ok(session):
                member_session = session
                assert False, "Why Login Success?"
            case Err(e):
                self.assertEqual(e, "비밀번호가 틀렸습니다.")
            case e:
                assert False, f"DB Error? : {e}"

        match self.login_service.login("qawsars", "123"):
            case Ok((session, _)):
                member_session = session
            case e:
                assert False, f"{e}"
        # 주문조회
        match self.read_order_service.get_order_data_for_buyer_page(
            member_session.get_id()
        ):
            case Ok((0, none)):
                self.assertEqual(len(none), 0)
            case e:
                assert False, f"{e}"

        # 상품 조회 및 선택
        match self.read_product_service.get_product_data_for_main_page(page=0, size=3):
            case Ok((_, products)):
                assert len(products) == 3, "Why Not Products num 3"
                target_product = products[0]
                self.assertIsInstance(target_product, Product)
            case e:
                assert False, f"{e}"

        # 상품 트랜젝션 생성
        match self.order_and_payment_service.publish_order_transition(
            recipient_name="Lee Takgyun",
            recipient_phone="01033452234",
            recipient_address="guri",
            product_id=target_product.id.get_id(),
            buy_count=3,
            single_price=target_product.price,
            user_session_key=member_session.get_id(),
        ):
            case Ok(trans):
                order_transition = trans
                order_price = trans.order.total_price
            case e:
                assert False, f"{e}"

        # 대금 확인 과정
        match self.order_and_payment_service.check_payment_price(
            order_transition.get_id(), order_price
        ):
            case Ok(True):
                pass
            case e:
                assert False, f"{e}"

        match self.order_and_payment_service.check_payment_price(
            order_transition.get_id(), order_price - 1000
        ):
            case Ok(False):
                pass
            case e:
                assert False, f"{e}"
        # 결제 완료
        match self.pay_service.approval_and_logging(
            order_transition,
            order_transition.order.total_price,
            "2222-2222-2222-2222",
        ):
            case Ok(True):
                pass
            case e:
                assert False, f"{e}"

        match self.order_and_payment_service.payment_and_approval_order(
            order_transition_session=order_transition.get_id(),
            payment_success=True,
        ):
            case Ok(id):
                order_id = id
            case e:
                assert False, f"{e}"
        # 주문조회
        match self.read_order_service.get_order_data_for_buyer_page(
            member_session.get_id()
        ):
            case Ok((1, orders)):
                self.assertEqual(len(orders), 1)

                target_order = orders[0]

                self.assertIsInstance(target_order, Order)
            case e:
                assert False, f"{e}"

        self.assertEqual(target_order.id.get_id(), order_id.get_id())
        self.assertEqual(target_order.recipient_name, "Lee Takgyun")
        self.assertEqual(target_order.recipient_address, "guri")
        self.assertEqual(target_order.recipient_phone, "01033452234")

        self.assertEqual(target_order.total_price, target_product.price * 3)
        self.assertEqual(target_order.buy_count, 3)
        self.assertEqual(target_order.product_name, target_product.name)
        self.assertEqual(target_order.product_id.get_id(), target_product.id.get_id())

        match self.order_and_payment_service.check_payment_price(
            order_transition.get_id(), 10000000000000000000000000000
        ):
            case Ok(a):
                assert False, f"Why Sucess:{a}"
            case Err("already payment."):
                pass
            case e:
                ic()
                assert False, f"{e}"

    def test_회원생성_주문조회_상품조회및선택_트렌젝션생성_Fail(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t\t", sys._getframe(0).f_code.co_name)
        # 회원 생성
        match self.member_create_service.create(
            account="arst",
            passwd="123",
            role="buyer",
            name="lee Tak",
            phone="01023459087",
            email="arst@daum.com",
            address="guri",
        ):
            case Ok(member_id):
                mid = member_id
            case _:
                assert False, "Fail Create Member"
        # login
        match self.login_service.login("arst", "134"):
            case Ok(session):
                member_session = session
                assert False, "Why Login Success?"
            case Err(e):
                self.assertEqual(e, "비밀번호가 틀렸습니다.")
            case e:
                assert False, f"DB Error? : {e}"

        match self.login_service.login("arst", "123"):
            case Ok((session, b)):
                member_session = session
                assert not b, f"change pw : {b}"
            case e:
                assert False, f"{e}"
        # 주문조회
        match self.read_order_service.get_order_data_for_buyer_page(
            member_session.get_id()
        ):
            case Ok((0, none)):
                self.assertEqual(len(none), 0)
            case e:
                assert False, f"{e}"

        # 상품 조회 및 선택
        match self.read_product_service.get_product_data_for_main_page(page=0, size=3):
            case Ok((_, products)):
                assert len(products) == 3, "Why Not Products num 3"
                target_product = products[0]
                self.assertIsInstance(target_product, Product)
            case e:
                assert False, f"{e}"

        # 상품 트랜젝션 생성
        match self.order_and_payment_service.publish_order_transition(
            recipient_name="Lee Takgyun",
            recipient_phone="01033452234",
            recipient_address="guri",
            product_id=target_product.id.get_id(),
            buy_count=1000,
            single_price=target_product.price,
            user_session_key=member_session.get_id(),
        ):
            case Ok(trans):
                order_transition = trans
                order_price = order_transition.order.total_price
            case e:
                assert False, f"{e}"

        # 대금 확인 과정
        match self.order_and_payment_service.check_payment_price(
            order_transition.get_id(), 1000
        ):
            case Ok(False):
                pass
            case e:
                assert False, f"{e}"

        match self.order_and_payment_service.check_payment_price(
            order_transition.get_id(), -100
        ):
            case Ok(False):
                pass
            case e:
                assert False, f"{e}"

        match self.order_and_payment_service.check_payment_price(
            order_transition.get_id(), 1000000000000000000000000000000000000
        ):
            case Ok(False):
                pass
            case e:
                assert False, f"{e}"

        # 결제 완료
        match self.pay_service.approval_and_logging(
            order_transition,
            order_transition.order.total_price,
            "1111-1111-1111-1111",
        ):
            case Err("Insufficient funds in the card"):
                pass
            case e:
                assert False, f"{e}"

        match self.order_and_payment_service.payment_and_approval_order(
            order_transition_session=order_transition.get_id(),
            payment_success=False,
        ):
            case Err("Fail Payment") | Err("Payment False"):
                pass
            case e:
                assert False, f"{e}"
        # 주문조회
        match self.read_order_service.get_order_data_for_buyer_page(
            member_session.get_id()
        ):
            case Ok((0, orders)):
                self.assertEqual(len(orders), 0)
            case e:
                assert False, f"{e}"

    def test_회원생성_주문조회_상품조회및선택_트렌젝션생성_결제완료_주문조회_판매자_판매조회(
        self,
    ):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t\t", sys._getframe(0).f_code.co_name)
        product_service = self.product_create_service
        # 회원 생성
        match self.member_create_service.create(
            account="sars123",
            passwd="123",
            role="buyer",
            name="lee Tak",
            phone="01023459087",
            email="arst@daum.com",
            address="guri",
        ):
            case Ok(member_id):
                mid = member_id
            case e:
                ic(e)
                assert False, "Fail Create Member"
        # login
        match self.login_service.login("sars123", "123"):
            case Ok((session, _)):
                member_session = session
            case e:
                assert False, f"{e}"

        match self.login_service.login("1q2w", "123"):
            case Ok((auth, b)):
                seller_session = auth
                assert not b, f"change pw : {b}"
            case _:
                assert False, "fail"

        # Create Product
        match product_service.publish_temp_product_id(seller_session.get_id()):
            case Ok(session):
                key_session = session
            case e:
                print(e)
                assert False, "False"

        match product_service.check_upload_image_path(
            "img01.png", key_session.get_id()
        ):
            case Ok(_):
                ...
            case e:
                ic(e)
                print(e)
                assert False, "False"

        match product_service.upload_product_data(
            product_name="쿠첸",
            price=12341,
            description="쿠쿠하세요. 쿠쿠",
            product_key=key_session.get_id(),
        ):
            case Ok(_):
                ...
            case e:
                ic(e)
                assert False, "False"

        match product_service.create(key_session.get_id()):
            case Ok(id):
                product_id = id
            case e:
                ic(e)
                assert False, "False"

        # member_id 주문조회
        match self.read_order_service.get_order_data_for_buyer_page(
            member_session.get_id()
        ):
            case Ok((0, none)):
                self.assertEqual(len(none), 0)
            case e:
                assert False, f"{e}"

        match self.read_order_service.get_order_data_for_seller_page(
            seller_session.get_id()
        ):
            case Ok((max, seller_orders)):
                before_max = max
            case e:
                assert False, f"{e}"
        # 상품 조회 및 선택
        match self.read_product_service.get_product_data_for_main_page(page=0, size=3):
            case Ok((_, products)):
                assert len(products) == 3, "Why Not Products num 3"
                target_product = products[0]
                self.assertIsInstance(target_product, Product)
                self.assertEqual(target_product.id.get_id(), product_id.get_id())
            case e:
                assert False, f"{e}"

        # 상품 트랜젝션 생성
        match self.order_and_payment_service.publish_order_transition(
            recipient_name="Lee Takgyun",
            recipient_phone="01033452234",
            recipient_address="guri",
            product_id=target_product.id.get_id(),
            buy_count=3,
            single_price=target_product.price,
            user_session_key=member_session.get_id(),
        ):
            case Ok(trans):
                order_transition = trans
            case e:
                assert False, f"{e}"

        # 결제 완료
        match self.pay_service.approval_and_logging(
            order_transition,
            order_transition.order.total_price,
            "2222-2222-2222-2222",
        ):
            case Ok(True):
                pass
            case e:
                assert False, f"{e}"

        match self.order_and_payment_service.payment_and_approval_order(
            order_transition_session=order_transition.get_id(),
            payment_success=True,
        ):
            case Ok(id):
                order_id = id
            case e:
                assert False, f"{e}"
        # Member 주문조회
        match self.read_order_service.get_order_data_for_buyer_page(
            member_session.get_id()
        ):
            case Ok((1, member_orders)):
                self.assertEqual(len(member_orders), 1)

                member_order = member_orders[0]

                self.assertIsInstance(member_order, Order)
            case e:
                assert False, f"{e}"

        self.assertEqual(member_order.id.get_id(), order_id.get_id())
        self.assertEqual(member_order.recipient_name, "Lee Takgyun")
        self.assertEqual(member_order.recipient_address, "guri")
        self.assertEqual(member_order.recipient_phone, "01033452234")

        self.assertEqual(member_order.total_price, target_product.price * 3)
        self.assertEqual(member_order.buy_count, 3)
        self.assertEqual(member_order.product_name, target_product.name)
        self.assertEqual(member_order.product_id.get_id(), target_product.id.get_id())

        # Seller 주문조회
        match self.read_order_service.get_order_data_for_seller_page(
            seller_session.get_id()
        ):
            case Ok((max, seller_orders)):
                self.assertEqual(before_max + 1, max)

                seller_order = seller_orders[0]

                self.assertEqual(seller_order, member_order)
            case e:
                assert False, f"{e}"


def main():
    unittest.main()


if __name__ == "__main__":
    main()
