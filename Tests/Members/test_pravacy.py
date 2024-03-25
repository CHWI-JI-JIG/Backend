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
from init_data import init_member
from get_config_data import get_db_padding, set_db_padding

import time

from icecream import ic


class test_privacy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = "test"
        print(sys._getframe(0).f_code.co_name, f"(test_privacy)")
        test_padding = "test_privacy_"
        set_db_padding(test_padding)
        cls.user_migrate = MySqlCreateUser(get_db_padding())
        cls.session_migrate = MySqlCreateSession(get_db_padding())
        cls.mysql_save_member = MySqlSaveMember(get_db_padding())
        cls.create_service = CreateMemberService(cls.mysql_save_member)
        cls.l_repo = MySqlLoginAuthentication(get_db_padding())
        cls.session_repo = MySqlLoadSession(get_db_padding())

        pravacy_repo = MySqlGetPrivacy(get_db_padding())
        cls.read_privacy = ReadPrivacyService(
            read_repo=pravacy_repo, load_session_repo=cls.session_repo
        )

        login = AuthenticationMemberService(
            auth_member_repo=MySqlLoginAuthentication(get_db_padding()),
            session_repo=MySqlMakeSaveMemberSession(get_db_padding()),
        )

        cls.login_service = login
        if cls.user_migrate.check_exist_user():
            cls.user_migrate.delete_user()

        cls.session_migrate.create_session()
        cls.user_migrate.create_user()
        init_member()

    @classmethod
    def tearDownClass(cls):
        "Hook method for deconstructing the class fixture after running all tests in the class."
        print(sys._getframe(0).f_code.co_name)
        if cls.session_migrate.check_exist_session():
            cls.session_migrate.delete_session()
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
            role="seller",
            name="Lee hohun",
            phone="010566788874",
            email="vacst@naver.com",
            address="서울시 광진구",
            company_registration_number="115557936219463",
            pay_account="6795943585566187",
        )

        match self.login_service.login("GreenGroveOrganics", "1234"):
            case Ok(session):
                self.login_session = session
            case e:
                ic()
                ic(e)
                assert False, f"{e}"

    def tearDown(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t", sys._getframe(0).f_code.co_name)
        if self.user_migrate.check_exist_user():
            self.user_migrate.delete_user()

    def test_pravacy1(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t\t", sys._getframe(0).f_code.co_name)
        # 로그인
        match self.login_service.login("1q2w2e34r", "456"):
            case Ok((session,b)):
                login_session = session
                assert not b, f"change pw : {b}"
            case e:
                assert False, f"{e}"

        # 로그인 한정보로 프라이버시 받기
        match self.read_privacy.read_privacy(login_session.get_id()):
            case Ok(p):
                privacy = p
                assert isinstance(privacy, Privacy), "Privacy"
            case e:
                assert False, f"{e}"

        self.assertEqual(
            privacy.address,
            "서울시 광진구",
        )

        self.assertEqual(
            privacy.email,
            "vacst@naver.com",
        )
        self.assertEqual(
            privacy.name,
            "Lee hohun",
        )
        self.assertEqual(
            privacy.phone,
            "010566788874",
        )
        self.assertEqual(
            privacy.id,
            login_session.member_id,
        )
        self.assertEqual(
            privacy.company_registration_number,
            "115557936219463",
        )
        self.assertEqual(
            privacy.pay_account,
            "6795943585566187",
        )


def main():
    unittest.main()


if __name__ == "__main__":
    main()
