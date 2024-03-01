import __init__
import unittest
import sys


from Storages.Comments import *
from Domains.Comments import *
from Applications.Members import *
from Storages.Members import *
from Storages.Sessions import *
from Storages.Comments import *

from Applications.Comments import *

from Migrations import MySqlCreateComments, MySqlCreateProduct, MySqlCreateUser
from result import Result, Ok, Err, is_ok

from icecream import ic

from init_data import *
from get_config_data import *


class test_comment(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = "test"
        print(sys._getframe(0).f_code.co_name, f"(test_comment)")
        test_padding = "test_comment_service"
        set_db_padding(test_padding)
        
        m_c = MySqlCreateComments(get_db_padding())
        cls.comment_migrate = m_c
        
        m_p = MySqlCreateProduct(get_db_padding())
        cls.product_migrate = m_p
        
        m_m = MySqlCreateUser(get_db_padding())
        cls.member_migrate = m_m
        
        if m_c.check_exist_comments():
            m_c.delete_comments()
        if m_p.check_exist_product():
            m_p.delete_product()
        if m_m.check_exist_user():
            m_m.check_exist_user
            
        m_m.create_user()
        init_member()
        
        m_p.create_product()
        init_product()
        
        cls.comment_create_service = CreateCommentService(
            save_comment=MySqlSaveComment(get_db_padding()),
            load_session=MySqlLoadSession(get_db_padding())
        )
        
        cls.comment_read_service = ReadOrderService(
            get_comment_repo=MySqlGetComment(get_db_padding()),
        )
        
        login = AuthenticationMemberService(
            auth_member_repo=LoginVerifiableAuthentication(get_db_padding()),
            session_repo=MakeSaveMemberSession(get_db_padding()),
        )
        cls.login_service = login

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
        if m_c.check_exist_comments():
            m_c.delete_comments()
        if m_p.check_exist_product():
            m_p.delete_product()
        if m_m.check_exist_user():
            m_m.check_exist_user
        

    def setUp(self):
        "Hook method for setting up the test fixture before exercising it."
        print("\t", sys._getframe(0).f_code.co_name)
        # 코멘트 테이블 생성 기본 세팅
        
        # 코멘트 테이블 생성 여부 확인
        assert self.comment_migrate.check_exist_comments(), "Not Init Comment table"
        # 제품 테이블 생성 여부 확인
        assert not self.product_migrate.check_exist_product(), "Exist Product table"
        self.comment_migrate.create_comments()
        init_comment()
        

    def tearDown(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t", sys._getframe(0).f_code.co_name)
        # 코멘트 테이블 삭제
        if self.comment_migrate.check_exist_comments():
            self.comment_migrate.delete_comments()
        init_comment()
        
        
        # self.comment_create_service.create_question(
        #     question="aaaaaa",
        #     product_id=product_list[0],
        #     user_key=self.key,
        # )
        # self.comment_create_service.create_question(
        #     question="bbbbbb",
        #     product_id=product_list[0],
        #     user_key=self.key,
        # )
        # self.comment_create_service.create_question(
        #     question="ccccccccc",
        #     product_id=product_list[0],
        #     user_key=self.key,
        # )
        # self.comment_create_service.create_question(
        #     question="ddddddddd",
        #     product_id=product_list[0],
        #     user_key=self.key,
        # )
        # self.comment_create_service.create_question(
        #     question="cccccccccchhhhhhhhhhh",
        #     product_id=product_list[0],
        #     user_key=self.key,
        # )
        # self.comment_create_service.create_question(
        #     question="aasdfhertbdfv",
        #     product_id=product_list[0],
        #     user_key=self.key,
        # )
        # self.comment_create_service.create_question(
        #     question="qwwerfgffghmdfgndfgb",
        #     product_id=product_list[0],
        #     user_key=self.key,
        # )
# 
    def test_comment_detail_page(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t\t", sys._getframe(0).f_code.co_name)
        reversed_comments = comment_list[:]
        reversed_comments.reverse()
        
        page=0
        size=3
        ret = self.comment_read_service.get_comment_data_for_product_page(
            page=page,
            size=size,
        )
        match ret:
            case Ok((max, comments)):
                self.assertEqual(len(reversed_comments), max)
                f, l = (page * size, page * size + size)
                l = l if l < max else -1

                for v, i in zip(reversed_comments[f:l], comments):
                    self.assertEqual(v.get_id(), i.id.get_id())
            case Err:
                assert False, "false"
                
        page=1
        size=3
        ret = self.comment_read_service.get_comment_data_for_product_page(
            page=page,
            size=size,
        )
        match ret:
            case Ok((max, comments)):
                self.assertEqual(len(reversed_comments), max)
                f, l = (page * size, page * size + size)
                l = l if l < max else -1

                for v, i in zip(reversed_comments[f:l], comments):
                    self.assertEqual(v.get_id(), i.id.get_id())
            case Err:
                assert False, "false"
    
                       


def main():
    unittest.main()


if __name__ == "__main__":
    main()
