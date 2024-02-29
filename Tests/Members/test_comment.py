from Applications.Comments import CreateCommentService
from Applications.Members import CreateMemberService
from Storages.Members import MySqlSaveMember
from Storages.Sessions import MySqlLoadSession
import __init__
import unittest
import sys


from Storages.Comments import *
from Domains.Comments import *

from Migrations import MySqlCreateComments, MySqlCreateProduct, MySqlCreateUser
from result import Result, Ok, Err, is_ok

from icecream import ic

from init_data import *


class test_comment(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = "test"
        print(sys._getframe(0).f_code.co_name, f"(test_comment)")
        test_padding = "test_comment_service"
        
        m_c = MySqlCreateComments(test_padding)
        cls.comment_migrate = m_c
        
        m_p = MySqlCreateProduct(test_padding)
        cls.product_migrate = m_p
        
        m_m = MySqlCreateUser(test_padding)
        cls.member_migrate = m_m
        
        # cls.mysql_save_comment = MySqlCreateComments(test_padding)
        # cls.create_comment = MySqlCreateComments(test_padding)
        
        # cls.l_repo = LoginVerifiableAuthentication(test_padding)
        # if cls.comment_migrate.check_exist_user():
        #     cls.comment_migrate.delete_user()
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
            save_comment=MySqlCreateComments(test_padding),
            load_session=MySqlLoadSession(test_padding)
        )

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
        

    def tearDown(self):``
        "Hook method for deconstructing the test fixture after testing it."
        print("\t", sys._getframe(0).f_code.co_name)
        # 코멘트 테이블 삭제
        if self.comment_migrate.check_exist_comments():
            self.comment_migrate.delete_comments()
        
        
        self.comment_create_service.create_question(
            question="aaaaaa",
            product_id=product_list[0],
            
        )

    def test_comment_detail_page(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t\t", sys._getframe(0).f_code.co_name)
        reversed_comments = comment_list[:]
        reversed_comments.reverse()
        
        page=0
        size=3
        ret = self.comment_create_service.get_comment_data_for_detail_page(
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
        ret = self.comment_create_service.get_comment_data_for_detail_page(
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
```