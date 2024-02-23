import __init__
import unittest
import sys


from Builders.Members import *
from Storages.Members import MySqlSaveMember
from Domains.Members import *

from Migrations import MySqlCreateUser, MySqlCreateProduct
from Applications.Members import CreateMemberService

from icecream import ic


class test_member_service(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = "test"
        print(sys._getframe(0).f_code.co_name, f"(test_member_service)")
        test_padding = "test_member_service_"
        cls.user_migrate = MySqlCreateUser(test_padding)
        # product_migrate = MySqlCreateProduct(test_padding)
        cls.mysql_save_member = MySqlSaveMember(test_padding)
        cls.create_service = CreateMemberService(cls.mysql_save_member)
        if cls.user_migrate.check_exist_user():
            cls.user_migrate.delete_user()

    @classmethod
    def tearDownClass(cls):
        "Hook method for deconstructing the class fixture after running all tests in the class."
        print(sys._getframe(0).f_code.co_name)
        if cls.user_migrate.check_exist_user():
            cls.user_migrate.delete_user()

    def setUp(self):
        "Hook method for setting up the test fixture before exercising it."
        print("\t", sys._getframe(0).f_code.co_name)
        self.create_service.create(
            account="abrst",
            passwd="123",
            role="buyer",
            name="Lee Takgun",
            phone="01036574774",
            email="vacst@naver.com",
            address="서울시 구로구",
            company_registration_number="023581466218612",
            pay_account="11255023855641233",
        )
        self.create_service.create(
            account="abrst",
            passwd="123",
            role="seller",
            name="Lee Takgun",
            phone="01036574774",
            email="vacst@naver.com",
            address="서울시 구로구",
            company_registration_number="023581466218612",
            pay_account="11255023855641233",
        )
        self.create_service.create(
            account="hohorst",
            passwd="456",
            role="seller",
            name="Lee hohun",
            phone="010566788874",
            email="vacst@naver.com",
            address="서울시 광진구",
            company_registration_number="115557936219463",
            pay_account="6795943585566187",
        )

    def tearDown(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t", sys._getframe(0).f_code.co_name)

    def test_pw_builder1(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t\t", sys._getframe(0).f_code.co_name)
        
    
    def test_user_join(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t\t", sys._getframe(0).f_code.co_name)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
