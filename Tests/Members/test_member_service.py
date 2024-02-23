import __init__
import unittest
import sys


from Builders.Members import *
from Storages.Members import MySqlSaveMember, LoginVerifiableAuthentication
from Domains.Members import *

from Migrations import MySqlCreateUser, MySqlCreateProduct
from Applications.Members import CreateMemberService
from Applications.Members.ExtentionMethod import hashing_passwd
from result import Result, Ok, Err, is_ok

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
        cls.l_repo = LoginVerifiableAuthentication(test_padding)
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
        if self.user_migrate.check_exist_user():
            self.user_migrate.delete_user()

    def test_정상_회원(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t\t", sys._getframe(0).f_code.co_name)

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

        self.assertIsInstance(uid, Ok)
        login_result = self.l_repo.identify_and_authenticate(
            "seller1", hashing_passwd("123456")
        )
        match login_result:
            case Ok(auth):
                self.assertTrue(auth.is_sucess)
            case Err:
                raise ValueError()

        # Create buyer
        uid = self.create_service.create(
            account="buyer1",
            passwd="12345",
            role="buyer",
            name="이고객",
            phone="01054561234",
            email="buyer@naver.com",
            address="서울시 서초구",
        )

        self.assertIsInstance(uid, Ok)
        login_result = self.l_repo.identify_and_authenticate(
            "buyer1", hashing_passwd("12345")
        )
        match login_result:
            case Ok(auth):
                self.assertTrue(auth.is_sucess)
            case Err:
                raise ValueError()

    def test_비정상_회원(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t\t", sys._getframe(0).f_code.co_name)

        # Create seller
        uid = self.create_service.create(
            account="1q2w2e34r",
            passwd="654321",
            role="seller",
            name="김셀러",
            phone="01085146951",
            email="sellerhi@naver.com",
            address="서울시 성동구",
            company_registration_number="1466555462",
            pay_account="11255023855444523",
        )
        self.assertIsInstance(uid, Err)

        # Create buyer
        uid = self.create_service.create(
            account="zxcvbn",
            passwd="987654",
            role="buyer",
            name="김고객",
            phone="01058612453",
            email="buyerhi@naver.com",
            address="서울시 동작구",
        )
        self.assertIsInstance(uid, Err)

    def test_로그인_성공(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t\t", sys._getframe(0).f_code.co_name)
        
        login_result = self.l_repo.identify_and_authenticate('qazwsx',hashing_passwd('123'))
        match login_result:
            case Ok(auth):
                self.assertEqual(auth.fail_count, 0)
                ret = self.l_repo.update_access(auth)
                self.assertEqual(auth.is_sucess,True)
                ft=auth.last_access
                self.assertIsNone(ret.ok())
            case Err:
                self.assertFalse(True)

        login_result = self.l_repo.identify_and_authenticate('qazwsx',hashing_passwd('123'))
        match login_result:
            case Ok(auth):
                self.assertEqual(auth.fail_count, 0)
                ret = self.l_repo.update_access(auth)
                self.assertEqual(auth.is_sucess,True)
                st=auth.last_access
                self.assertIsNone(ret.ok())
            case Err:
                self.assertFalse(True)
                
        self.assertTrue(ft < st)
                      
        
        
        

    def test_로그인_실패(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t\t", sys._getframe(0).f_code.co_name)

        # seller (비밀번호 불일치 = 실패)
        login_result = self.l_repo.identify_and_authenticate(
            "qazwsx", hashing_passwd("123--")
        )
        match login_result:
            case Ok(auth):
                self.assertEqual(auth.fail_count, 0)
                ret = self.l_repo.update_access(auth)
                self.assertIsNone(ret.ok())
            case Err:
                self.assertFalse(True)

        # (비밀번호 불일치 = 실패)
        login_result = self.l_repo.identify_and_authenticate(
            "qazwsx", hashing_passwd("123--")
        )
        match login_result:
            case Ok(auth):
                self.assertEqual(auth.fail_count, 1)  # 위에서 실패해서 +1
                ret = self.l_repo.update_access(auth)
                self.assertIsNone(ret.ok())
            case Err:
                self.assertFalse(True)

        # (비밀번호 일치 = 성공)
        login_result = self.l_repo.identify_and_authenticate(
            "qazwsx", hashing_passwd("123")
        )
        match login_result:
            case Ok(auth):
                self.assertEqual(auth.fail_count, 2)  # 위에서 실패해서 +1
                ret = self.l_repo.update_access(auth)
                self.assertIsNone(ret.ok())
            case Err:
                self.assertFalse(True)

        # (비밀번호 불일치 = 실패)
        login_result = self.l_repo.identify_and_authenticate(
            "qazwsx", hashing_passwd("123--")
        )
        match login_result:
            case Ok(auth):
                self.assertEqual(auth.fail_count, 0)  # 위에서 성공해서 0
                ret = self.l_repo.update_access(auth)
                self.assertIsNone(ret.ok())
            case Err:
                self.assertFalse(True)

        # buyer (비밀번호 불일치 = 실패)
        login_result = self.l_repo.identify_and_authenticate(
            "zxcvbn", hashing_passwd("123--")
        )
        match login_result:
            case Ok(auth):
                self.assertEqual(auth.fail_count, 0)
                ret = self.l_repo.update_access(auth)
                self.assertIsNone(ret.ok())
            case Err:
                self.assertFalse(True)

        # (비밀번호 불일치 = 실패)
        login_result = self.l_repo.identify_and_authenticate(
            "zxcvbn", hashing_passwd("123--")
        )
        match login_result:
            case Ok(auth):
                self.assertEqual(auth.fail_count, 1)  # 위에서 실패해서 +1
                ret = self.l_repo.update_access(auth)
                self.assertIsNone(ret.ok())
            case Err:
                self.assertFalse(True)

        # (비밀번호 일치 = 성공)
        login_result = self.l_repo.identify_and_authenticate(
            "zxcvbn", hashing_passwd("123")
        )
        match login_result:
            case Ok(auth):
                self.assertEqual(auth.fail_count, 2)  # 위에서 실패해서 +1
                ret = self.l_repo.update_access(auth)
                self.assertIsNone(ret.ok())
            case Err:
                self.assertFalse(True)

        # (비밀번호 불일치 = 실패)
        login_result = self.l_repo.identify_and_authenticate(
            "zxcvbn", hashing_passwd("123--")
        )
        match login_result:
            case Ok(auth):
                self.assertEqual(auth.fail_count, 0)  # 위에서 성공해서 0
                ret = self.l_repo.update_access(auth)
                self.assertIsNone(ret.ok())
            case Err:
                self.assertFalse(True)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
