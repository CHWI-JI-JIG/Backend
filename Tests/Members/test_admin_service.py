import __init__
import unittest
import sys


from Builders.Members import *
from Storages.Members import *
from Domains.Members import *

from Migrations import *
from Applications.Members import *
from Applications.Members.ExtentionMethod import hashing_passwd
from result import Result, Ok, Err, is_ok

import time
from get_config_data import set_db_padding, get_db_padding

from icecream import ic


class test_admin_service(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = "test"
        print(sys._getframe(0).f_code.co_name, f"(test_admin_service)")
        test_padding = "test_admin_service_"
        set_db_padding(test_padding)
        cls.user_migrate = MySqlCreateUser(get_db_padding())
        cls.mysql_save_member = MySqlSaveMember(get_db_padding())
        cls.create_service = CreateMemberService(cls.mysql_save_member)
        cls.l_repo = MySqlLoginAuthentication(get_db_padding())
        cls.get_repo = MySqlGetMember(get_db_padding())
        cls.edit_repo = MySqlEditMember(get_db_padding())
        cls.admin_service = AdminService(cls.get_repo, cls.edit_repo)
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
        self.user_migrate.create_user()
        self.create_service.create(
            account="zxcvbn",
            passwd="123",
            role="buyer",
            name="Lee Takgun",
            phone="01036574774",
            email="vacst@naver.com",
            address="서울시 구로구",
        )
        self.create_service.create(
            account="qazwsx",
            passwd="123",
            role="seller",
            name="이탁균",
            phone="01036826974",
            email="hdegut@naver.com",
            address="서울시 구로구",
            company_registration_number="023581466218612",
            pay_account="11255023855641233",
        )
        self.create_service.create(
            account="1q2w2e34r",
            passwd="456",
            role="buyer",
            name="Lee hohun",
            phone="010566788874",
            email="cvast@naver.com",
            address="서울시 광진구",
        )
        self.create_service.create(
            account="admin",
            passwd="456",
            role="admin",
            name="이호연",
            phone="01067384874",
            email="asvct@naver.com",
            address="서울시 광진구",
        )

    def tearDown(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t", sys._getframe(0).f_code.co_name)
        if self.user_migrate.check_exist_user():
            self.user_migrate.delete_user()

    def test_관리자_회원(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t\t", sys._getframe(0).f_code.co_name)
        # login
        match self.l_repo.identify_and_authenticate(
            "admin",
            hashing_passwd("456"),
        ):
            case Ok(auth):
                self.assertTrue(auth.is_sucess)
                admin_auto = auth
            case Err:
                raise ValueError()

        # get members
        ic()
        ic("Not Auth Setting")
        match self.admin_service.read_members(
            page=0,
            size=10,
        ):
            case Ok((max, members)):
                assert max == 4, f"user num is {max}!!"
                seller_num = len(
                    list(filter(lambda member: member.role == RoleType.SELLER, members))
                )
                assert seller_num == 1, f"seller is {seller_num}"
                members = members
            case e:
                ic(e)
                assert False, "Fail load member"

        for buyer in filter(lambda member: member.role == RoleType.BUYER, members):
            match self.admin_service.change_role(RoleType.SELLER, buyer.id.get_id()):
                case Ok(_):
                    ...
                case e:
                    ic(e)
                    assert False, "Fail change role."

        # Create seller
        uid = self.create_service.create(
            account="seller1",
            passwd="123456",
            role="seller",
            name="김쟌느",
            phone="01012349876",
            email="seller@naver.com",
            address="서울시 동작구",
            company_registration_number="1466215462",
            pay_account="11255023855646523",
        )

        # get members
        ic()
        ic("Not Auth Setting")
        match self.admin_service.read_members(
            page=0,
            size=10,
        ):
            case Ok((max, members)):
                assert max == 5, "user num is 5!!"
                seller_num = len(
                    list(filter(lambda member: member.role == RoleType.SELLER, members))
                )
                assert seller_num == 4, "seller is 4"
                members = members
            case e:
                ic(e)
                assert False, "Fail load member"

        for buyer in filter(lambda member: member.role == RoleType.SELLER, members):
            match self.admin_service.change_role(RoleType.BUYER, buyer.id.get_id()):
                case Ok(_):
                    ...
                case e:
                    ic(e)
                    assert False, "Fail change role."

        # get members
        ic()
        ic("Not Auth Setting")
        match self.admin_service.read_members(
            page=0,
            size=10,
        ):
            case Ok((max, members)):
                assert max == 5, "user num is 5!!"
                seller_num = len(
                    list(filter(lambda member: member.role == RoleType.BUYER, members))
                )
                assert seller_num == 4, "seller is 4"
                members = members
            case e:
                ic(e)
                assert False, "Fail load member"

    def test_비정상_회원(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t\t", sys._getframe(0).f_code.co_name)
        # login
        match self.l_repo.identify_and_authenticate(
            "admin",
            hashing_passwd("456"),
        ):
            case Ok(auth):
                self.assertTrue(auth.is_sucess)
                admin_auto = auth
            case Err:
                raise ValueError()

        # get members
        ic()
        ic("Not Auth Setting")
        match self.admin_service.read_members(
            page=0,
            size=10,
        ):
            case Ok((max, members)):
                assert max == 4, "user num is 4!!"
                seller_num = len(
                    list(filter(lambda member: member.role == RoleType.SELLER, members))
                )
                assert seller_num == 1, "seller is 1"
                members = members
            case e:
                ic(e)
                assert False, "Fail load member"

        for buyer in filter(lambda member: member.role == RoleType.BUYER, members):
            match self.admin_service.change_role(RoleType.SELLER, buyer.id.get_id()):
                case Ok(_):
                    ...
                case e:
                    ic(e)
                    assert False, "Fail change role."

        match self.admin_service.change_role(RoleType.SELLER, admin_auto.id.get_id()):
            case Ok(_):
                ...
            case e:
                ic(e)
                assert False, "Fail change role."

        # Create seller
        uid = self.create_service.create(
            account="seller1",
            passwd="123456",
            role="seller",
            name="김쟌느",
            phone="01012349876",
            email="seller@naver.com",
            address="서울시 동작구",
            company_registration_number="1466215462",
            pay_account="11255023855646523",
        )

        # get members
        ic()
        ic("Not Auth Setting")
        match self.admin_service.read_members(
            page=0,
            size=10,
        ):
            case Ok((max, members)):
                assert max == 5, "user num is 5!!"
                seller_num = len(
                    list(filter(lambda member: member.role == RoleType.SELLER, members))
                )
                assert seller_num == 5, "seller is 5"
                members = members
            case e:
                ic(e)
                assert False, "Fail load member"

        # login
        ic()
        ic("Not Auth Setting")
        match self.l_repo.identify_and_authenticate(
            "admin",
            hashing_passwd("456"),
        ):
            case Ok(auth):
                self.assertTrue(auth.is_sucess)
                admin_auto = auth
            case Err:
                raise ValueError()

        for buyer in filter(lambda member: member.role == RoleType.SELLER, members):
            match self.admin_service.change_role(RoleType.BUYER, buyer.id.get_id()):
                case Ok(_):
                    assert False, "Permission Error : change role."
                case e:
                    ...

        # get members
        ic()
        ic("Not Auth Setting")
        match self.admin_service.read_members(
            page=0,
            size=10,
        ):
            case Ok(_):
                assert False, "Permission Error : change role."
            case e:
                ...


def main():
    unittest.main()


if __name__ == "__main__":
    main()