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
from Storages.Sessions import *


from get_config_data import get_db_padding, set_db_padding
from init_data import member_list, product_list, init_member, init_product

from icecream import ic


class test_product_service(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = "test"
        print(sys._getframe(0).f_code.co_name, f"(test_product_service)")

        set_db_padding("test_product_service_")

        m_m = MySqlCreateUser(get_db_padding())
        cls.user_migrate = m_m
        m_p = MySqlCreateProduct(get_db_padding())
        cls.product_migrate = m_p
        ms = MySqlCreateSession(get_db_padding())
        cls.session_migrate = ms

        if ms.check_exist_session():
            ms.delete_session()
        if m_p.check_exist_product():
            m_p.delete_product()
        if m_m.check_exist_user():
            m_m.delete_user()

        service = CreateMemberService(MySqlSaveMember(get_db_padding()))
        cls.member_create_service = service

        login = AuthenticationMemberService(
            auth_member_repo=LoginVerifiableAuthentication(get_db_padding()),
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

        m_m.create_user()
        init_member()
        ms.create_session()

    @classmethod
    def tearDownClass(cls):
        "Hook method for deconstructing the class fixture after running all tests in the class."
        print(sys._getframe(0).f_code.co_name)
        if cls.session_migrate.check_exist_session():
            cls.session_migrate.delete_session()
        if cls.product_migrate.check_exist_product():
            cls.product_migrate.delete_product()
        if cls.user_migrate.check_exist_user():
            cls.user_migrate.delete_user()

    def setUp(self):
        "Hook method for setting up the test fixture before exercising it."
        print("\t", sys._getframe(0).f_code.co_name)
        assert self.user_migrate.check_exist_user(), "Not Init User table"
        assert not self.product_migrate.check_exist_product(), "Exsist Product table"
        self.product_migrate.create_product()
        init_product()

    def tearDown(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t", sys._getframe(0).f_code.co_name)
        if self.product_migrate.check_exist_product():
            self.product_migrate.delete_product()

    def test_아이디발급_이미지등록후_상품정보_올리고_상품등록(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t\t", sys._getframe(0).f_code.co_name)
        service = self.product_create_service

        login = self.login_service

        match login.login("1q2w", "123"):
            case Ok(auth):
                key = auth.get_id()
            case _:
                assert False, "fail"

        match service.publish_temp_product_id(key):
            case Ok(session):
                key_session = session
            case _:
                assert False, "False"

        match service.check_upload_image_path("img.jpg", key_session.get_id()):
            case Ok(_):
                ...
            case e:
                ic(e)
                assert False, "False"

        match service.create(key_session.get_id()):
            case Ok(id):
                id = id
            case _:
                assert False, "False"

        match self.product_read_service.get_product_for_detail_page(id.get_id()):
            case product if isinstance(product, Product):
                pass
            case _:
                assert False, "False"

    def test_아이디발급_상품정보_올리고_상품등록(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t\t", sys._getframe(0).f_code.co_name)

    def test_product_main_page(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t\t", sys._getframe(0).f_code.co_name)
        reversed_products = product_list[:]
        reversed_products.reverse()

        page = 0
        size = 3
        ret = self.product_read_service.get_product_data_for_main_page(
            page=page,
            size=size,
        )
        match ret:
            case Ok((max, products)):
                self.assertEqual(len(reversed_products), max)
                f, l = (page * size, page * size + size)
                l = l if l < max else -1

                for v, i in zip(reversed_products[f:l], products):
                    self.assertEqual(v.get_id(), i.id.get_id())
            case Err:
                assert False, "false"

        page = 1
        size = 3
        ret = self.product_read_service.get_product_data_for_main_page(
            page=page,
            size=size,
        )
        match ret:
            case Ok((max, products)):
                self.assertEqual(len(reversed_products), max)
                f, l = (page * size, page * size + size)
                l = l if l < max else -1

                for v, i in zip(reversed_products[f:l], products):
                    self.assertEqual(v.get_id(), i.id.get_id())
            case Err:
                assert False, "false"

        page = 1
        size = 3
        ret = self.product_read_service.get_product_data_for_main_page(
            page=page,
            size=size,
        )
        match ret:
            case Ok((max, products)):
                self.assertEqual(len(reversed_products), max)
                f, l = (page * size, page * size + size)
                l = l if l < max else -1

                for v, i in zip(reversed_products[f:l], products):
                    self.assertEqual(v.get_id(), i.id.get_id())
            case Err:
                assert False, "false"

        page = 2
        size = 3
        ret = self.product_read_service.get_product_data_for_main_page(
            page=page,
            size=size,
        )
        match ret:
            case Ok((max, products)):
                self.assertEqual(len(reversed_products), max)
                f, l = (page * size, page * size + size)
                l = l if l < max else -1

                for v, i in zip(reversed_products[f:l], products):
                    self.assertEqual(v.get_id(), i.id.get_id())
            case Err:
                assert False, "false"

        page = 3
        size = 3
        ret = self.product_read_service.get_product_data_for_main_page(
            page=page,
            size=size,
        )
        match ret:
            case Ok((max, products)):
                self.assertEqual(len(reversed_products), max)
                f, l = (page * size, page * size + size)
                l = l if l < max else -1

                for v, i in zip(reversed_products[f:l], products):
                    self.assertEqual(v.get_id(), i.id.get_id())
            case Err:
                assert False, "false"

        page = 4
        size = 3
        ret = self.product_read_service.get_product_data_for_main_page(
            page=page,
            size=size,
        )
        match ret:
            case Ok((max, products)):
                self.assertEqual(len(reversed_products), max)
                f, l = (page * size, page * size + size)
                l = l if l < max else -1

                for v, i in zip(reversed_products[f:l], products):
                    self.assertEqual(v.get_id(), i.id.get_id())
            case Err:
                assert False, "false"

        page = 5
        size = 3
        ret = self.product_read_service.get_product_data_for_main_page(
            page=page,
            size=size,
        )
        match ret:
            case Ok((max, products)):
                self.assertEqual(len(reversed_products), max)
                f, l = (page * size, page * size + size)
                l = l if l < max else -1

                for v, i in zip(reversed_products[f:l], products):
                    self.assertEqual(v.get_id(), i.id.get_id())
            case Err:
                assert False, "false"

    def test_product_seller_page(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t\t", sys._getframe(0).f_code.co_name)
        target_id = member_list[0].get_id()
        list_o: List[ProductID] = [
            product_list[0],
            product_list[2],
            product_list[5],
            product_list[6],
            product_list[7],
            product_list[9],
            product_list[11],
        ]

        login = self.login_service

        match login.login("1q2w", "123"):
            case Ok(auth):
                key = auth.get_id()
            case _:
                assert False, "fail"

        page = 0
        size = 10
        ret = self.product_read_service.get_product_data_for_seller_page(
            seller_id=target_id,
            user_key=key,
            page=page,
            size=size,
        )
        match ret:
            case Ok((max, products)):
                f, l = (page * size, page * size + size)
                l = l if l < max else -1
                self.assertEqual(max, len(list_o))
                for i, v in zip(products, list_o):
                    self.assertEqual(i.id.get_id(), v.get_id())

            case Err:
                assert False, "false"

    def test_product_seller_page_다른_아이디로접속시도(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t\t", sys._getframe(0).f_code.co_name)
        target_id = member_list[0].get_id()
        list_o: List[ProductID] = [
            product_list[0],
            product_list[2],
            product_list[5],
            product_list[6],
            product_list[7],
            product_list[9],
            product_list[11],
        ]

        login = self.login_service

        match login.login("vbvb", "12"):
            case Ok(auth):
                key = auth.get_id()
            case _:
                assert False, "fail"

        page = 0
        size = 10
        ret = self.product_read_service.get_product_data_for_seller_page(
            seller_id=target_id,
            user_key=key,
            page=page,
            size=size,
        )
        match ret:
            case Err("NotOnwer"):
                pass
            case _:
                assert False, "False"


def main():
    unittest.main()


if __name__ == "__main__":
    main()
