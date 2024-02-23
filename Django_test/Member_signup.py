import __init__
import unittest
from Applications.Members.CreateMemberService import CreateMemberService
from Storages.Members.MySqlSaveMember import MySqlSaveMember
from Domains.Members import Member, Privacy, Authentication

class TestSignup(unittest.TestCase):
    def test_successful_signup(self):
        # 회원 가입에 필요한 임의의 데이터 설정
        account = "user123"
        passwd = "password123"
        role = "buyer"
        name = "John Doe"
        phone = "123456789"
        email = "john@example.com"
        
        # CreateMemberService 인스턴스 생성
        create_member_service = CreateMemberService(MySqlSaveMember())

        # 회원 가입 시도
        result = create_member_service.create(
            account, passwd, role, name, phone, email
        )

        # 결과 확인
        self.assertTrue(result.is_ok())

    # def test_failed_signup(self):
    #     # 회원 가입에 필요한 임의의 데이터 설정 (실패하는 케이스)
    #     account = "user123"
    #     passwd = "password123"
    #     role = "buyer"
    #     name = "John Doe"
    #     phone = "123456789"
    #     email = "john@example.com"
        
    #     # CreateMemberService 인스턴스 생성
    #     create_member_service = CreateMemberService(MySqlSaveMember())

    #     # 회원 가입 시도
    #     result = create_member_service.create(
    #         account, passwd, role, name, phone, email
    #     )

    #     # 결과 확인
    #     self.assertFalse(result.is_ok())


if __name__ == '__main__':
    unittest.main()