import time
import __init__
from datetime import datetime, timedelta
from uuid import UUID, uuid4
import unittest
import sys

from Commons.format import KOREA_TIME_FORMAT
from Domains.Members import *
from Domains.Sessions import *
from Domains.Products import *
from Domains.Orders import *
from Builders.Members import *
from Builders.Products import *
from Builders.Orders import *
from Applications.Members.ExtentionMethod import hashing_passwd
from Applications.Sessions.SessionHelper import check_valide_session
from icecream import ic


class test_builder(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = "test"
        print(sys._getframe(0).f_code.co_name, f"(test_test_builder)")

    @classmethod
    def tearDownClass(cls):
        "Hook method for deconstructing the class fixture after running all tests in the class."
        print(sys._getframe(0).f_code.co_name)

    def setUp(self):
        "Hook method for setting up the test fixture before exercising it."
        print("\t", sys._getframe(0).f_code.co_name)

    def tearDown(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t", sys._getframe(0).f_code.co_name)

    def test_pw_builder1(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t\t", sys._getframe(0).f_code.co_name)
        a = "aaaa"
        builder = NoFilterMemberBuilder().set_passwd(a)
        b = builder.passwd
        self.assertEqual(a, b)

    def test_pw_builder2(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t\t", sys._getframe(0).f_code.co_name)
        a = "aaaa"
        builder = NoFilterMemberBuilder(passwd_converter=hashing_passwd).set_passwd(a)
        b = builder.passwd
        self.assertNotEqual(a, b)

    def test_member_session(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t\t", sys._getframe(0).f_code.co_name)
        id = "d697b39f733a426f96a13fc40c8bf061"
        mid = "1297b39f733a421296a13fc40c8bf012"
        member_id = MemberIDBuilder().set_uuid(id).unwrap().build()
        new_session = (
            MemberSessionBuilder()
            .set_key()
            .unwrap()
            .set_member_id(id)
            .unwrap()
            .set_role("buyer")
            .set_name("이탁균")
            .set_use_count()
            .set_owner_id(mid)
            .unwrap()
            .set_create_time()
            .build()
        )
        self.assertEqual(
            '{"member_id": "d697b39f733a426f96a13fc40c8bf061", "name": "이탁균", "role": "buyer"}',
            new_session.serialize_value(),
        )

        read_session = (
            MemberSessionBuilder()
            .set_deserialize_key(new_session.get_id())
            .set_deserialize_value(make_session_token(new_session))
            .unwrap()
            .build()
        )
        self.assertEqual(new_session, read_session)

        read_session = (
            MemberSessionBuilder()
            .set_deserialize_key(new_session.get_id())
            .set_deserialize_value(make_session_token(new_session))
            .unwrap()
            .build()
        )
        self.assertEqual(new_session, read_session)

    def test_session_valide_사용_횟수_늘려버려(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t\t", sys._getframe(0).f_code.co_name)
        id = "d697b39f733a426f96a13fc40c8bf061"
        seller_id = "82090bfba6d04a84a669c2a97c0ef283"
        buyer_id = "365b77a0a6b34fe28c7112d6c1bb64ca"
        mid = "1297b39f733a421296a13fc40c8bf012"

        # Set Session
        buyer_ID = MemberIDBuilder().set_uuid(buyer_id).unwrap().build()

        buyer_session = MemberSession(
            key=uuid4(),
            owner_id=UUID(hex=buyer_id),
            create_time=datetime.now().replace(microsecond=0),
            use_count=20,
            name="이탁균",
            role=RoleType.BUYER,
            member_id=buyer_ID,
            max_count=1,
            minute=10,
        )
        self.assertEqual(
            '{"member_id": "365b77a0a6b34fe28c7112d6c1bb64ca", "name": "이탁균", "role": "buyer"}',
            buyer_session.serialize_value(),
        )

        member_id = MemberIDBuilder().set_uuid(seller_id).unwrap().build()
        seller_session = MemberSession(
            key=uuid4(),
            owner_id=UUID(hex=seller_id),
            create_time=datetime.now().replace(microsecond=0),
            use_count=20,
            name="이호연",
            role=RoleType.SELLER,
            member_id=member_id,
            max_count=1,
            minute=10,
        )
        self.assertEqual(
            '{"member_id": "82090bfba6d04a84a669c2a97c0ef283", "name": "이호연", "role": "seller"}',
            seller_session.serialize_value(),
        )

        product_id = ProductIDBuilder().set_uuid(id).unwrap().build()
        product_session = ProductTempSession(
            key=uuid4(),
            owner_id=seller_session.key,
            create_time=datetime.now().replace(microsecond=0),
            use_count=20,
            seller_id=member_id,
            product=Product(
                id=product_id,
                seller_id=member_id,
                img_path="img01.png",
                name="오븐",
                price=9513,
                description="이 오븐은 효율적이고 안전한 방식으로 음식을 구워줍니다.",
                register_day=datetime.now().replace(microsecond=0),
            ),
            max_count=5,
            minute=10,
        )
        self.assertEqual(
            r'{"check_product": true, "check_img": false, "seller_id": "82090bfba6d04a84a669c2a97c0ef283", "name": "오븐", "price": 9513, "description": "이 오븐은 효율적이고 안전한 방식으로 음식을 구워줍니다."}',
            product_session.serialize_value(),
        )

        order_id = OrderIDBuilder().set_uuid(uuid4()).unwrap().build()
        order_transition = OrderTransitionSession(
            key=order_id.uuid,
            owner_id=buyer_session.key,
            create_time=datetime.now().replace(microsecond=0),
            use_count=20,
            order=Order(
                id=order_id,
                product_id=product_id,
                buyer_id=buyer_ID,
                recipient_name="test name",
                recipient_phone="01033458312",
                recipient_address="guri suteak",
                product_name=product_session.product.name,
                product_img_path="img01.png",
                buy_count=3,
                total_price=9513 * 3,
                order_date=datetime.now().replace(microsecond=0),
            ),
            max_count=5,
            minute=10,
        )
        self.assertEqual(
            '{"check_success": false, "buyer_id": "365b77a0a6b34fe28c7112d6c1bb64ca", "recipient_name": "test name", "recipient_phone": "01033458312", "recipient_address": "guri suteak", "product_id": "d697b39f733a426f96a13fc40c8bf061", "buy_count": 3, "total_price": 28539}',
            order_transition.serialize_value(),
        )

        # 1. 사용 횟수 늘려버려!

        # Check
        self.assertFalse(check_valide_session(buyer_session), f"{buyer_session}")
        self.assertFalse(check_valide_session(seller_session), f"{seller_session}")
        self.assertFalse(check_valide_session(product_session), f"{product_session}")
        self.assertFalse(check_valide_session(order_transition), f"{order_transition}")

    def test_session_valide_가능_분을_줄여서_테스트_해라(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t\t", sys._getframe(0).f_code.co_name)
        id = "d697b39f733a426f96a13fc40c8bf061"
        seller_id = "82090bfba6d04a84a669c2a97c0ef283"
        buyer_id = "365b77a0a6b34fe28c7112d6c1bb64ca"
        mid = "1297b39f733a421296a13fc40c8bf012"
        # Set Session
        buyer_ID = MemberIDBuilder().set_uuid(buyer_id).unwrap().build()

        buyer_session = MemberSession(
            key=uuid4(),
            use_count=0,
            owner_id=UUID(hex=buyer_id),
            create_time=datetime.now() - timedelta(minutes=1),
            name="이탁균",
            role=RoleType.BUYER,
            member_id=buyer_ID,
            minute=1,
        )
        self.assertEqual(
            '{"member_id": "365b77a0a6b34fe28c7112d6c1bb64ca", "name": "이탁균", "role": "buyer"}',
            buyer_session.serialize_value(),
        )

        member_id = MemberIDBuilder().set_uuid(seller_id).unwrap().build()
        seller_session = MemberSession(
            key=uuid4(),
            use_count=0,
            owner_id=UUID(hex=seller_id),
            create_time=datetime.now() - timedelta(minutes=1),
            name="이호연",
            role=RoleType.SELLER,
            member_id=member_id,
            minute=1,
        )
        self.assertEqual(
            '{"member_id": "82090bfba6d04a84a669c2a97c0ef283", "name": "이호연", "role": "seller"}',
            seller_session.serialize_value(),
        )

        product_id = ProductIDBuilder().set_uuid(id).unwrap().build()
        product_session = ProductTempSession(
            key=uuid4(),
            owner_id=seller_session.key,
            seller_id=member_id,
            create_time=datetime.now() - timedelta(minutes=1),
            use_count=0,
            product=Product(
                id=product_id,
                seller_id=member_id,
                img_path="img01.png",
                name="오븐",
                price=9513,
                description="이 오븐은 효율적이고 안전한 방식으로 음식을 구워줍니다.",
                register_day=datetime.now().replace(microsecond=0),
            ),
            minute=1,
        )
        self.assertEqual(
            r'{"check_product": true, "check_img": false, "seller_id": "82090bfba6d04a84a669c2a97c0ef283", "name": "오븐", "price": 9513, "description": "이 오븐은 효율적이고 안전한 방식으로 음식을 구워줍니다."}',
            product_session.serialize_value(),
        )

        order_id = OrderIDBuilder().set_uuid(uuid4()).unwrap().build()
        order_transition = OrderTransitionSession(
            key=order_id.uuid,
            owner_id=buyer_session.key,
            create_time=datetime.now() - timedelta(minutes=1),
            use_count=0,
            order=Order(
                id=order_id,
                product_id=product_id,
                buyer_id=buyer_ID,
                recipient_name="test name",
                recipient_phone="01033458312",
                recipient_address="guri suteak",
                product_name=product_session.product.name,
                product_img_path="img01.png",
                buy_count=3,
                total_price=9513 * 3,
                order_date=datetime.now().replace(microsecond=0),
            ),
            minute=1,
        )
        self.assertEqual(
            '{"check_success": false, "buyer_id": "365b77a0a6b34fe28c7112d6c1bb64ca", "recipient_name": "test name", "recipient_phone": "01033458312", "recipient_address": "guri suteak", "product_id": "d697b39f733a426f96a13fc40c8bf061", "buy_count": 3, "total_price": 28539}',
            order_transition.serialize_value(),
        )

        # 2. 가능 분을 줄여서 테스트 해라
        time.sleep(1)
        # Check
        self.assertFalse(check_valide_session(buyer_session), f"{buyer_session}")
        self.assertFalse(check_valide_session(seller_session), f"{seller_session}")
        self.assertFalse(check_valide_session(product_session), f"{product_session}")
        self.assertFalse(check_valide_session(order_transition), f"{order_transition}")

    def test_session_valide_둘다_틀리게_해서_테스트_해라(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t\t", sys._getframe(0).f_code.co_name)
        id = "d697b39f733a426f96a13fc40c8bf061"
        seller_id = "82090bfba6d04a84a669c2a97c0ef283"
        buyer_id = "365b77a0a6b34fe28c7112d6c1bb64ca"
        mid = "1297b39f733a421296a13fc40c8bf012"
        # Set Session
        buyer_ID = MemberIDBuilder().set_uuid(buyer_id).unwrap().build()

        buyer_session = MemberSession(
            key=uuid4(),
            owner_id=UUID(hex=buyer_id),
            create_time=datetime.now() - timedelta(minutes=1),
            use_count=20,
            name="이탁균",
            role=RoleType.BUYER,
            member_id=buyer_ID,
            max_count=1,
            minute=10,
        )
        self.assertEqual(
            '{"member_id": "365b77a0a6b34fe28c7112d6c1bb64ca", "name": "이탁균", "role": "buyer"}',
            buyer_session.serialize_value(),
        )

        member_id = MemberIDBuilder().set_uuid(seller_id).unwrap().build()
        seller_session = MemberSession(
            key=uuid4(),
            owner_id=UUID(hex=seller_id),
            create_time=datetime.now() - timedelta(minutes=1),
            use_count=20,
            name="이호연",
            role=RoleType.SELLER,
            member_id=member_id,
            max_count=1,
            minute=10,
        )
        self.assertEqual(
            '{"member_id": "82090bfba6d04a84a669c2a97c0ef283", "name": "이호연", "role": "seller"}',
            seller_session.serialize_value(),
        )

        product_id = ProductIDBuilder().set_uuid(id).unwrap().build()
        product_session = ProductTempSession(
            key=uuid4(),
            owner_id=seller_session.key,
            create_time=datetime.now() - timedelta(minutes=1),
            use_count=20,
            seller_id=member_id,
            product=Product(
                id=product_id,
                seller_id=member_id,
                img_path="img01.png",
                name="오븐",
                price=9513,
                description="이 오븐은 효율적이고 안전한 방식으로 음식을 구워줍니다.",
                register_day=datetime.now().replace(microsecond=0),
            ),
            max_count=5,
            minute=10,
        )
        self.assertEqual(
            r'{"check_product": true, "check_img": false, "seller_id": "82090bfba6d04a84a669c2a97c0ef283", "name": "오븐", "price": 9513, "description": "이 오븐은 효율적이고 안전한 방식으로 음식을 구워줍니다."}',
            product_session.serialize_value(),
        )

        order_id = OrderIDBuilder().set_uuid(uuid4()).unwrap().build()
        order_transition = OrderTransitionSession(
            key=order_id.uuid,
            owner_id=buyer_session.key,
            create_time=datetime.now() - timedelta(minutes=1),
            use_count=20,
            order=Order(
                id=order_id,
                product_id=product_id,
                buyer_id=buyer_ID,
                recipient_name="test name",
                recipient_phone="01033458312",
                recipient_address="guri suteak",
                product_name=product_session.product.name,
                product_img_path="img01.png",
                buy_count=3,
                total_price=9513 * 3,
                order_date=datetime.now().replace(microsecond=0),
            ),
            max_count=5,
            minute=10,
        )
        self.assertEqual(
            '{"check_success": false, "buyer_id": "365b77a0a6b34fe28c7112d6c1bb64ca", "recipient_name": "test name", "recipient_phone": "01033458312", "recipient_address": "guri suteak", "product_id": "d697b39f733a426f96a13fc40c8bf061", "buy_count": 3, "total_price": 28539}',
            order_transition.serialize_value(),
        )

        # 3. 둘다 틀리게 해서 테스트 해라
        time.sleep(1)

        # Check
        self.assertFalse(check_valide_session(buyer_session), f"{buyer_session}")
        self.assertFalse(check_valide_session(seller_session), f"{seller_session}")
        self.assertFalse(check_valide_session(product_session), f"{product_session}")
        self.assertFalse(check_valide_session(order_transition), f"{order_transition}")

    def test_session_valide_양호하게_해서_테스트_해라(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t\t", sys._getframe(0).f_code.co_name)
        id = "d697b39f733a426f96a13fc40c8bf061"
        seller_id = "82090bfba6d04a84a669c2a97c0ef283"
        buyer_id = "365b77a0a6b34fe28c7112d6c1bb64ca"
        mid = "1297b39f733a421296a13fc40c8bf012"
        # Set Session
        buyer_ID = MemberIDBuilder().set_uuid(buyer_id).unwrap().build()

        buyer_session = MemberSession(
            key=uuid4(),
            owner_id=UUID(hex=buyer_id),
            create_time=datetime.now().replace(microsecond=0) - timedelta(seconds=55),
            use_count=9,
            name="이탁균",
            role=RoleType.BUYER,
            member_id=buyer_ID,
            max_count=10,
            minute=1,
        )
        self.assertEqual(
            '{"member_id": "365b77a0a6b34fe28c7112d6c1bb64ca", "name": "이탁균", "role": "buyer"}',
            buyer_session.serialize_value(),
        )

        member_id = MemberIDBuilder().set_uuid(seller_id).unwrap().build()
        seller_session = MemberSession(
            key=uuid4(),
            owner_id=UUID(hex=seller_id),
            create_time=datetime.now().replace(microsecond=0) - timedelta(seconds=55),
            use_count=9,
            name="이호연",
            role=RoleType.SELLER,
            member_id=member_id,
            max_count=10,
            minute=1,
        )
        self.assertEqual(
            '{"member_id": "82090bfba6d04a84a669c2a97c0ef283", "name": "이호연", "role": "seller"}',
            seller_session.serialize_value(),
        )

        product_id = ProductIDBuilder().set_uuid(id).unwrap().build()
        product_session = ProductTempSession(
            key=uuid4(),
            owner_id=seller_session.key,
            create_time=datetime.now().replace(microsecond=0) - timedelta(seconds=55),
            use_count=9,
            seller_id=member_id,
            product=Product(
                id=product_id,
                seller_id=member_id,
                img_path="img01.png",
                name="오븐",
                price=9513,
                description="이 오븐은 효율적이고 안전한 방식으로 음식을 구워줍니다.",
                register_day=datetime.now().replace(microsecond=0),
            ),
            max_count=10,
            minute=1,
        )
        self.assertEqual(
            r'{"check_product": true, "check_img": false, "seller_id": "82090bfba6d04a84a669c2a97c0ef283", "name": "오븐", "price": 9513, "description": "이 오븐은 효율적이고 안전한 방식으로 음식을 구워줍니다."}',
            product_session.serialize_value(),
        )

        order_id = OrderIDBuilder().set_uuid(uuid4()).unwrap().build()
        order_transition = OrderTransitionSession(
            key=order_id.uuid,
            owner_id=buyer_session.key,
            create_time=datetime.now().replace(microsecond=0) - timedelta(seconds=55),
            use_count=9,
            order=Order(
                id=order_id,
                product_id=product_id,
                buyer_id=buyer_ID,
                recipient_name="test name",
                recipient_phone="01033458312",
                recipient_address="guri suteak",
                product_name=product_session.product.name,
                product_img_path="img01.png",
                buy_count=3,
                total_price=9513 * 3,
                order_date=datetime.now().replace(microsecond=0),
            ),
            max_count=10,
            minute=1,
        )
        self.assertEqual(
            '{"check_success": false, "buyer_id": "365b77a0a6b34fe28c7112d6c1bb64ca", "recipient_name": "test name", "recipient_phone": "01033458312", "recipient_address": "guri suteak", "product_id": "d697b39f733a426f96a13fc40c8bf061", "buy_count": 3, "total_price": 28539}',
            order_transition.serialize_value(),
        )

        # 4. 양호하게 해서 테스트 해라
        time.sleep(1)

        # Check
        self.assertTrue(check_valide_session(buyer_session), f"{buyer_session}")
        self.assertTrue(check_valide_session(seller_session), f"{seller_session}")
        self.assertTrue(check_valide_session(product_session), f"{product_session}")
        self.assertTrue(check_valide_session(order_transition), f"{order_transition}")


def main():
    unittest.main()


if __name__ == "__main__":
    main()
