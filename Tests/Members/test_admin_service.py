import __init__
import unittest
import sys


from Builders.Members import *
from Storages.Members import *
from Storages.Sessions import *
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
        ms = MySqlCreateSession(get_db_padding())
        cls.session_migrate = ms
        otp = MySqlCreateOtp(get_db_padding())
        cls.otp_migrate = otp

        cls.user_migrate = MySqlCreateUser(get_db_padding())
        cls.mysql_save_member = MySqlSaveMember(get_db_padding())
        cls.create_service = CreateMemberService(cls.mysql_save_member)
        cls.l_repo = MySqlLoginAuthentication(get_db_padding())
        cls.get_repo = MySqlGetMember(get_db_padding())
        cls.edit_repo = MySqlEditMember(get_db_padding())
        cls.load_session = MySqlLoadSession(get_db_padding())
        cls.admin_service = AdminService(cls.get_repo, cls.edit_repo, cls.load_session)

        auth_member_repo = MySqlLoginAuthentication(get_db_padding())
        session_repo = MySqlMakeSaveMemberSession(get_db_padding())
        otp_session_repo = TempMySqlMakeSaveMemberSession(get_db_padding())
        otp_load_session_repo = TempMySqlLoadSession(get_db_padding())
        load_repo = MySqlLoadSession(get_db_padding())
        del_session_repo = MySqlDeleteSession(get_db_padding())

        cls.abmin_login_service = LoginAdminService(
            auth_member_repo,
            session_repo,
            load_repo,
            del_session_repo,
            otp_session_repo,
            otp_load_session_repo,
        )
        cls.login_service = AuthenticationMemberService(
            auth_member_repo=cls.l_repo,
            session_repo=MySqlMakeSaveMemberSession(get_db_padding()),
            load_repo=MySqlLoadSession(get_db_padding()),
            del_session_repo=MySqlDeleteSession(get_db_padding()),
        )

        if ms.check_exist_session():
            ms.delete_session()
        if cls.user_migrate.check_exist_user():
            cls.user_migrate.delete_user()

    @classmethod
    def tearDownClass(cls):
        "Hook method for deconstructing the class fixture after running all tests in the class."
        print(sys._getframe(0).f_code.co_name)
        if cls.session_migrate.check_exist_session():
            cls.session_migrate.delete_session()
        if cls.otp_migrate.check_exist_otps():
            cls.otp_migrate.check_exist_otps()
        if cls.user_migrate.check_exist_user():
            cls.user_migrate.delete_user()

    def setUp(self):
        "Hook method for setting up the test fixture before exercising it."
        print("\t", sys._getframe(0).f_code.co_name)
        self.session_migrate.create_session()
        self.otp_migrate.create_otp()
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
        if self.otp_migrate.check_exist_otps():
            self.otp_migrate.check_exist_otps()

    def test_Not_관리자_회원(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t\t", sys._getframe(0).f_code.co_name)
        match self.login_service.login("admin", "456"):
            case Ok((auth, b)):
                raise ValueError()
            case e:
                pass

    def test_관리자_회원(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t\t", sys._getframe(0).f_code.co_name)
        # login
        match self.abmin_login_service.login("admin", "456"):
            case Ok(auth):
                admin_auth = auth
            case e:
                ic(e)
                raise ValueError()

        match self.abmin_login_service.otp_login(admin_auth.get_id()):
            case Ok(auth):
                admin_auth = auth
            case e:
                ic(e)
                raise ValueError()

        # get members
        match self.admin_service.read_members(
            admin_key=admin_auth.get_id(),
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
            match self.admin_service.change_role(
                admin_key=auth.get_id(),
                role=RoleType.SELLER,
                target_user_id=buyer.id.get_id(),
            ):
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
        match self.admin_service.read_members(
            admin_key=admin_auth.get_id(),
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
            match self.admin_service.read_members(
                admin_key=admin_auth.get_id(),
                page=0,
                size=10,
            ):
                case Ok(_):
                    ...
                case e:
                    ic(e)
                    assert False, "Fail change role."

        # get members
        match self.admin_service.read_members(
            admin_key=admin_auth.get_id(),
            page=0,
            size=10,
        ):
            case Ok((max, members)):
                assert max == 5, f"user num is {max}!!"
                seller_num = len(
                    list(filter(lambda member: member.role == RoleType.SELLER, members))
                )
                assert seller_num == 4, f"seller is {seller_num}"
                members = members
            case e:
                ic(e)
                assert False, "Fail load member"

    def test_비정상_회원(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t\t", sys._getframe(0).f_code.co_name)
        # login
        match self.abmin_login_service.login("admin", "456"):
            case Ok(auth):
                admin_auth = auth
            case e:
                ic(e)
                raise ValueError()

        match self.abmin_login_service.otp_login(admin_auth.get_id()):
            case Ok(auth):
                admin_auth = auth
            case e:
                ic(e)
                raise ValueError()
        # get members
        match self.admin_service.read_members(
            admin_key=admin_auth.get_id(),
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
            match self.admin_service.change_role(
                admin_key=admin_auth.get_id(),
                role=RoleType.SELLER,
                target_user_id=buyer.id.get_id(),
            ):
                case Ok(_):
                    ...
                case e:
                    ic(e)
                    assert False, "Fail change role."

        match self.admin_service.change_role(
            admin_key=admin_auth.get_id(),
            role=RoleType.SELLER,
            target_user_id=admin_auth.member_id.get_id(),
        ):
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
        match self.admin_service.read_members(
            admin_key=admin_auth.get_id(),
            page=0,
            size=10,
        ):
            case Ok((max, members)):
                assert max == 5, "user num is 5!!"
                seller_num = len(
                    list(filter(lambda member: member.role == RoleType.SELLER, members))
                )
                assert seller_num == 5, f"seller is {seller_num}"
                members = members
            case e:
                ic(e)
                assert False, "Fail load member"

        # login
        match self.login_service.login("admin", "456"):
            case Ok((auth, b)):
                admin_auth = auth
                assert not b, f"change pw : {b}"
            case e:
                ic()
                ic(e)
                raise ValueError()

        for buyer in filter(lambda member: member.role == RoleType.SELLER, members):
            match self.admin_service.change_role(
                admin_key=auth.get_id(),
                role=RoleType.SELLER,
                target_user_id=buyer.id.get_id(),
            ):
                case Ok(_):
                    assert False, "Permission Error : change role."
                case e:
                    ...

        # get members
        match self.admin_service.read_members(
            admin_key=admin_auth.get_id(),
            page=0,
            size=10,
        ):
            case Ok(a):
                ic(a)
                assert False, "Permission Error : change role."
            case e:
                ...


def main():
    unittest.main()


if __name__ == "__main__":
    main()
