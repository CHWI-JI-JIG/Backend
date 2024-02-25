import __init__
import unittest  # import IsolatedAsyncioTestCase
import sys
from icecream import ic

from Migrations import MySqlCreateUser, MySqlCreateProduct, MySqlCreateSession

from Builders.Members import *
# from Storages.Members import MySqlSaveMember
from Domains.Sessions import MemberSession, ISesseionBuilder
from Domains.Members import *



class test_session_migrate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = "test"
        print(sys._getframe(0).f_code.co_name, f"(test_session_migrate)")
        ## 썼으면 삭제
        test_padding = "test_migrate_"
        cls.session_migrate = MySqlCreateSession(test_padding)
        cls.mysql_save_member = MySqlSaveMember(test_padding)
        cls.create_service = CreateMemberService(cls.mysql_save_member)
        cls.l_repo = LoginVerifiableAuthentication(test_padding)

        if cls.session_migrate.check_exist_session():
            cls.session_migrate.delete_session()



    @classmethod
    def tearDownClass(cls):
        "Hook method for deconstructing the class fixture after running all tests in the class."
        print(sys._getframe(0).f_code.co_name)

    def setUp(self):
        "Hook method for setting up the test fixture before exercising it."
        print("\t", sys._getframe(0).f_code.co_name)
        ## 썼으면 삭제

        ## 테이블이 없는지 확인
        self.assertFalse(self.session_migrate.check_exist_session())
        # self.assertFalse(self.product_migrate.check_exist_product())

    def tearDown(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t", sys._getframe(0).f_code.co_name)
        ## 썼으면 삭제
        # if self.product_migrate.check_exist_product():
        #     self.product_migrate.delete_product()
        if self.session_migrate.check_exist_session():
            self.session_migrate.delete_session()

        self.assertFalse(self.session_migrate.check_exist_session())
        # self.assertFalse(self.product_migrate.check_exist_product())



    def test_create_session(self): #완료
        "Hook method for deconstructing the test fixture after testing it."
        print("\t\t", sys._getframe(0).f_code.co_name)
        self.session_migrate.create_session()
        # self.product_migrate.create_product()
        self.assertTrue(self.session_migrate.check_exist_session())

    def test_create_session(self):
            "Hook method for deconstructing the test fixture after testing it."
            print("\t\t", sys._getframe(0).f_code.co_name)
            self.session_migrate.create_session()
            self.assertTrue(self.session_migrate.check_exist_session())

            ######## MySqlSaveMember.py 테스트코드 자리  #################
            id = ISesseionBuilder().set_deserialize_key().set_deserialize_value(1).build()
            id = MemberIDBuilder().set_uuid4().set_seqence(1).build()

            member = Member(id=id, account="jihee", passwd="jh1234@", role=RoleType.BUYER)
            privacy = Privacy(
                id=id,
                name="김지희",
                phone="01012345678",
                email="jihee@test.com",
                address="대한제국이여, 영원하라.",
            )

            authentication = Authentication(
                id=id, last_access="", fail_count=1, is_sucess=""
            )

            result = self.mysql_save_member.save_member(member, privacy)
            self.assertTrue(result)

            ####################################



def main():
    unittest.main()


if __name__ == "__main__":
    main()
