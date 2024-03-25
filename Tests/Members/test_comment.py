import __init__
import unittest
import sys


from Domains.Comments import *
from Domains.Products import *
from Builders.Products import *
from Builders.Comments import *
from Applications.Comments import *
from Applications.Products import *
from Applications.Members import *

from Storages.Comments import *
from Storages.Members import *
from Storages.Products import *
from Storages.Sessions import *
from Storages.Comments import *

from Migrations import *
from result import Result, Ok, Err, is_ok

from icecream import ic
from datetime import datetime

from init_data import init_member
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

        login = AuthenticationMemberService(
            auth_member_repo=MySqlLoginAuthentication(get_db_padding()),
            session_repo=MySqlMakeSaveMemberSession(get_db_padding()),
        )
        cls.login_service = login

        cls.comment_create_service = CreateCommentService(
            save_comment=MySqlSaveComment(get_db_padding()),
            load_session=MySqlLoadSession(get_db_padding()),
        )

        cls.comment_read_service = ReadCommentService(
            get_comment_repo=MySqlGetComment(get_db_padding()),
        )

        match login.login("dfdf", "123"):
            case Ok((auth, b)):
                cls.buyer_key = auth
                cls.buyer_id = auth.member_id
                assert not b, f"change pw : {b}"
            case Err(err):
                assert False, f"Login failed: {err}"

        match login.login("1q2w", "123"):
            case Ok((auth, b)):
                cls.seller_key = auth
                cls.seller_id = auth.member_id
                assert not b, f"change pw : {b}"
            case Err(err):
                assert False, f"Login failed: {err}"

        match login.login("SalesSphereSeller", "1234"):
            case Ok((auth, b)):
                cls.user_key = auth
                cls.user_id = auth.member_id
                assert not b, f"login : {b}"
            case Err(err):
                assert False, f"Login failed: {err}"
        m_p.create_product()

        create = MySqlSaveProduct(get_db_padding())

        id = ProductIDBuilder().set_uuid().unwrap().set_seqence(1).build()

        match create.save_product(
            Product(
                id=id,
                seller_id=cls.seller_id,
                name="쿠쿠밥솥",
                img_path="img.jpg",
                price="170000",
                description="쿠쿠하세요~ 쿠쿠.",
                register_day=datetime.now(),
            )
        ):
            case Ok(ret):
                cls.product = ret
            case a:
                assert False, f"Fail Create Member:{a}"

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
        # 코멘트 테이블 생성 여부 확인
        assert self.comment_migrate.check_exist_comments(), "Not Init Comment table"

    def tearDown(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t", sys._getframe(0).f_code.co_name)
        # 테스트 케이스마다 코멘트 테이블 삭제
        if self.comment_migrate.check_exist_comments():
            self.comment_migrate.delete_comments()

    def test_comment_create_question(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t\t", sys._getframe(0).f_code.co_name)

        # 테스트 이전의 comment 테이블의 행 수 저장
        comments_before = self.comment_read_service.get_comment_data_for_product_page(
            product_id=self.product.get_id(),
        ).unwrap()

        # 코멘트를 생성하고
        ret = self.comment_create_service.create_question(
            question="질문질문",
            product_id=self.product.get_id(),
            user_key=self.buyer_key.get_id(),
        ).unwrap()

        comments_after = self.comment_read_service.get_comment_data_for_product_page(
            product_id=self.product.get_id(),
        ).unwrap()

        self.assertEqual(comments_before[0] + 1, comments_after[0])

    def test_comment_update_answer(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t\t", sys._getframe(0).f_code.co_name)

        match self.comment_read_service.get_comment_data_for_product_page(
            product_id=self.product.get_id(),
            page=0,
            size=10,
        ):
            case Ok((max, _)):
                beforemax = max
            case e:
                assert False, f"{e}"

        # 1. 새로운 코멘트 생성
        ret_create = self.comment_create_service.create_question(
            question="질문질문",
            product_id=self.product.get_id(),
            user_key=self.buyer_key.get_id(),
        ).unwrap()

        # 2. owner 코멘트에 답변을 추가
        ret_answer = self.comment_create_service.add_answer(
            answer="답변답변",
            comment_id=ret_create.get_id(),  # 코멘트 생성 시 얻은 ID
            user_key=self.seller_key.get_id(),
        )
        self.assertTrue(is_ok(ret_answer), "답변 추가에 실패했습니다.")

        # 3. 업데이트된 코멘트를 다시 읽고 답변이 제대로 추가되었는지 확인
        ret_read_updated = self.comment_read_service.get_comment_data_for_product_page(
            product_id=self.product.get_id(),
            page=0,
            size=10,
        )
        match ret_read_updated:
            case Ok((max, comments_updated)):
                assert max == beforemax + 1, "max Error"
                target = comments_updated[0]
            case e:
                assert False, f"{e}"
        self.assertEqual(target.id.get_id(), ret_create.get_id())
        self.assertEqual(target.answer, "답변답변")
        self.assertEqual(target.question, "질문질문")

        # 4. not owner 코멘트에 답변을 추가
        ret_answer = self.comment_create_service.add_answer(
            answer="답변답변",
            comment_id=ret_create.get_id(),  # 코멘트 생성 시 얻은 ID
            user_key=self.user_key.get_id(),
        )

        # 5. 코멘트를 다시 읽고 답변이 확인
        ret_read_updated = self.comment_read_service.get_comment_data_for_product_page(
            product_id=self.product.get_id(),
            page=0,
            size=10,
        )
        match ret_read_updated:
            case Ok((max, comments_updated)):
                assert max == beforemax + 1, "max Error"
                target = comments_updated[0]
            case e:
                assert False, f"{e}"
        self.assertEqual(target.id, ret_create)
        self.assertEqual(target.answer, "답변답변")
        self.assertEqual(target.question, "질문질문")


def main():
    unittest.main()


if __name__ == "__main__":
    main()
