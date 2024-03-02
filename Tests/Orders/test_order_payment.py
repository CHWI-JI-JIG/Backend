import __init__
import unittest
import sys

from typing import List
from result import Result, Ok, Err
import copy

from Migrations import *

from Domains.Members import *
from Domains.Products import *
from Domains.Sessions import *

from Builders.Members import *
from Builders.Products import *

from Applications.Members.ExtentionMethod import hashing_passwd
from Applications.Members import CreateMemberService
from Applications.Products import *
from Applications.Members import *

from Storages.Members import *
from Storages.Products import *
from Storages.Orders import *
from Storages. import *
from Storages.Products import *
from Storages.Sessions import *


from get_config_data import get_db_padding, set_db_padding
from init_data import (
    member_list,
    product_list,
    init_member,
    init_product,
    init_comment,
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

        if ms.check_exist_session():
            ms.delete_session()
        if mo.check_exist_order():
            mo.delete_order()
        if mp.check_exist_product():
            mp.delete_product()
        if mm.check_exist_user():
            mm.delete_user()

        service = CreateMemberService(MySqlSaveMember(get_db_padding()))
        cls.member_create_service = service

        login = AuthenticationMemberService(
            auth_member_repo=MySqlLoginAuthentication(get_db_padding()),
            session_repo=MakeSaveMemberSession(get_db_padding()),
        )
        cls.login_service = login

        service = ReadProductService(
            get_product_repo=MySqlGetProduct(get_db_padding()),
            load_session_repo=MySqlLoadSession(get_db_padding()),
        )
        cls.product_read_service = service
        service = CreateProductService(
            save_product=MySqlSaveProduct(get_db_padding()),
            save_product_session=MySqlSaveProductTempSession(get_db_padding()),
            load_session=MySqlLoadSession(get_db_padding()),
        )
        cls.product_create_service = service
        
        service = AuthenticationMemberService(
            auth_member_repo=
            save_product=MySqlSaveProduct(get_db_padding()),
            save_product_session=MySqlSaveProductTempSession(get_db_padding()),
            load_session=MySqlLoadSession(get_db_padding()),
        )
        cls.product_create_service = service
        
        
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

    def test_회원생성_주문조회_상품조회및선택_트렌젝션생성_결제완료_주문조회(self):
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
        match self
        
        # 주문조회
        # 상품 조회 및 선택
        # 상품 트랜젝션 생성
        # 결제 완료
        # 주문조회


def main():
    unittest.main()


if __name__ == "__main__":
    main()
