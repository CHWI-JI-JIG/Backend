import __init__
import unittest
import sys


from Storages.Comments import *
from Domains.Comments import *
from Applications.Members import *
from Storages.Members import *
from Storages.Sessions import *
from Storages.Comments import *
from Builders.Comments import *
from Applications.Comments import *
from Migrations import *
from Applications.Comments import *
from result import Result, Ok, Err, is_ok

from icecream import ic

from init_data import *
from get_config_data import *


class test_comment(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = "test"
        print(sys._getframe(0).f_code.co_name, f"(test_comment)")
        test_padding = "test_comment_service_"
        set_db_padding(test_padding)
        
        m_c = MySqlCreateComments(get_db_padding())
        cls.comment_migrate = m_c
        
        m_p = MySqlCreateProduct(get_db_padding())
        cls.product_migrate = m_p
        
        m_m = MySqlCreateUser(get_db_padding())
        cls.member_migrate = m_m
        
        m_s = MySqlCreateSession(get_db_padding())
        cls.session_migrate = m_s
        
        if m_c.check_exist_comments():
            m_c.delete_comments()
        if m_p.check_exist_product():
            m_p.delete_product()
        if m_m.check_exist_user():
            m_m.delete_user()
        if m_s.check_exist_session():
            m_s.delete_session()
            
        m_m.create_user()
        init_member() 
        m_s.create_session()
        
        m_p.create_product()
        init_product()
        
        login = AuthenticationMemberService(
            auth_member_repo=LoginVerifiableAuthentication(get_db_padding()),
            session_repo=MakeSaveMemberSession(get_db_padding()),
        )
        cls.login_service = login
        
        cls.comment_create_service = CreateCommentService(
            save_comment=MySqlSaveComment(get_db_padding()),
            load_session=MySqlLoadSession(get_db_padding())
        )
        
        cls.comment_read_service = ReadCommentService(
            get_comment_repo=MySqlGetComment(get_db_padding()),
        )

        match login.login("1q2w", "123"):
            case Ok(auth):
                cls.user_id = auth.member_id
                cls.key = auth.get_id()
            case Err(err):
                assert False, f"Login failed: {err}"

    @classmethod
    def tearDownClass(cls):
        "Hook method for deconstructing the class fixture after running all tests in the class."
        print(sys._getframe(0).f_code.co_name)
        m_c = cls.comment_migrate
        m_p = cls.product_migrate
        m_m = cls.member_migrate
        m_s = cls.session_migrate
        
        if m_c.check_exist_comments():
            m_c.delete_comments()
        if m_p.check_exist_product():
            m_p.delete_product()
        if m_m.check_exist_user():
            m_m.delete_user()
        if m_s.check_exist_session():
            m_s.delete_session()
        

    def setUp(self):
        "Hook method for setting up the test fixture before exercising it."
        print("\t", sys._getframe(0).f_code.co_name)
        # 테스트 케이스마다 코멘트 테이블 생성
        if not self.comment_migrate.check_exist_comments():
            self.comment_migrate.create_comments()
            init_comment()
        # 코멘트 테이블 생성 여부 확인
        ic(self.comment_migrate.check_exist_comments())
        assert self.comment_migrate.check_exist_comments(), "Not Init Comment table"


    def tearDown(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t", sys._getframe(0).f_code.co_name)
        # 테스트 케이스마다 코멘트 테이블 삭제
        # if self.comment_migrate.check_exist_comments():
        #     self.comment_migrate.delete_comments()

    # def test_comment_detail_page(self):
    #     "Hook method for deconstructing the test fixture after testing it."
    #     print("\t\t", sys._getframe(0).f_code.co_name)
    #     # 테스트 데이터의 코멘트 수를 사용하여 예상한 코멘트 수 설정
    #     expected_comments_count = len(comment_list)
        
    #     # 코멘트 데이터를 조회하여 반환값을 확인
    #     ret = self.comment_read_service.get_comment_data_for_product_page(
    #         product_id='53eb346c07d144a0a7ee3c1257b4ea83',
    #         page=0,
    #         size=3,
    #     )
    #     match ret:
    #         case Ok((total_comments, comments)):
    #             # 실제 코멘트 수와 예상한 코멘트 수를 비교
    #             self.assertEqual(expected_comments_count, total_comments)
    #             # 추가적인 검증 코드 생략
    #         case Err:
    #             assert False, "false"
                
    # def test_comment_create_question(self):
    #         "Hook method for deconstructing the test fixture after testing it."
    #         print("\t\t", sys._getframe(0).f_code.co_name)
            
    #         # 테스트 이전의 comment 테이블의 행 수 저장
    #         comments_before = self.comment_read_service.get_comment_data_for_product_page(
    #             product_list[0].get_id(),
    #         )
            
    #         # 코멘트를 생성하고
    #         ret = self.comment_create_service.create_question(
    #             "질문질문",
    #             product_list[0].get_id(),
    #             self.key,
    #         )
            
    #         comments_after = self.comment_read_service.get_comment_data_for_product_page(
    #             product_list[0].get_id(), 
    #         )
            
    #         self.assertEqual(comments_before.unwrap()[0]+1, comments_after.unwrap()[0])
            
            
            
    def test_comment_update_answer(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t\t", sys._getframe(0).f_code.co_name)

        # 1. 새로운 코멘트 생성
        ret_create = self.comment_create_service.create_question(
            "질문질문",
            product_list[0].get_id(),
            self.key,
        )
        
        # 2. 코멘트에 답변을 추가
        ret_answer = self.comment_create_service.add_answer(
            answer="답변답변",
            comment_id=ret_create.unwrap().get_id(),  # 코멘트 생성 시 얻은 ID
            user_key=self.key,
        )
        self.assertTrue(is_ok(ret_answer), "답변 추가에 실패했습니다.")

        # 3. 업데이트된 코멘트를 다시 읽고 답변이 제대로 추가되었는지 확인
        ret_read_updated = self.comment_read_service.get_comment_data_for_product_page(
            product_id=product_list[0].get_id(),
            page=0,
            size=10, 
        )
        self.assertTrue(is_ok(ret_read_updated), "업데이트된 코멘트 읽기에 실패")
        _, comments_updated = ret_read_updated.unwrap()
        target = comments_updated[0]
        self.assertEqual(target.id, ret_create.unwrap())
        self.assertEqual(target.answer, "답변답변")
        self.assertEqual(target.question, "질문질문")






def main():
    unittest.main()


if __name__ == "__main__":
    main()
