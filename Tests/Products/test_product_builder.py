import __init__
import unittest
import sys

from Domains.Members import *
from Builders.Members import *
from Builders.Products import *
from Domains.Sessions import *
from Applications.Members.ExtentionMethod import hashing_passwd

from icecream import ic


class test_product_builder(unittest.TestCase):
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

    def test_product_session_이미지만(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t\t", sys._getframe(0).f_code.co_name)
        id = "d697b39f733a426f96a13fc40c8bf061"
        product_id = ProductIDBuilder().set_uuid(id).build()
        new_session = (
            ProductSessionBuilder()
            .set_img_path("img01.png")
            .unwrap()
            .set_key()
            .set_seller_id(id)
            .build()
        )
        self.assertEqual(
            '{"check_product": false, "check_img": true, "seller_id": "d697b39f733a426f96a13fc40c8bf061", "img_path": "img01.png"}',
            new_session.serialize_value(),
        )

        read_session = (
            ProductSessionBuilder()
            .set_deserialize_key(new_session.get_id())
            .set_deserialize_value(new_session.serialize_value())
            .unwrap()
            .build()
        )
        self.assertEqual(new_session, read_session)

    def test_product_session_상품만(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t\t", sys._getframe(0).f_code.co_name)
        id = "d697b39f733a426f96a13fc40c8bf061"

        product_id = ProductIDBuilder().set_uuid(id).build()
        new_session = (
            ProductSessionBuilder()
            .set_description("이 오븐은 효율적이고 안전한 방식으로 음식을 구워줍니다.")
            .set_seller_id("82090bfba6d04a84a669c2a97c0ef283")
            .set_name("오븐")
            .set_price(9513)
            .set_key()
            .build()
        )
        self.assertEqual(
            r'{"check_product": true, "check_img": false, "seller_id": "82090bfba6d04a84a669c2a97c0ef283", "name": "오븐", "price": 9513, "description": "이 오븐은 효율적이고 안전한 방식으로 음식을 구워줍니다."}',
            new_session.serialize_value(),
        )

        read_session = (
            ProductSessionBuilder()
            .set_deserialize_key(new_session.get_id())
            .set_deserialize_value(new_session.serialize_value())
            .unwrap()
            .build()
        )
        self.assertEqual(new_session.serialize_value(), read_session.serialize_value())

    def test_product_session_둘다(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t\t", sys._getframe(0).f_code.co_name)
        id = "d697b39f733a426f96a13fc40c8bf061"

        product_id = ProductIDBuilder().set_uuid(id).build()
        new_session = (
            ProductSessionBuilder()
            .set_description("이 오븐은 효율적이고 안전한 방식으로 음식을 구워줍니다.")
            .set_seller_id("82090bfba6d04a84a669c2a97c0ef283")
            .set_name("오븐")
            .set_price(9513)
            .set_img_path("img01.png")
            .unwrap()
            .set_key()
            .build()
        )
        self.assertEqual(
            r'{"check_product": true, "check_img": true, "seller_id": "82090bfba6d04a84a669c2a97c0ef283", "name": "오븐", "price": 9513, "description": "이 오븐은 효율적이고 안전한 방식으로 음식을 구워줍니다.", "img_path": "img01.png"}',
            new_session.serialize_value(),
        )

        read_session = (
            ProductSessionBuilder()
            .set_deserialize_key(new_session.get_id())
            .set_deserialize_value(new_session.serialize_value())
            .unwrap()
            .build()
        )
        self.assertEqual(new_session.serialize_value(), read_session.serialize_value())

    def test_product_session_상품_후_이미지(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t\t", sys._getframe(0).f_code.co_name)
        id = "d697b39f733a426f96a13fc40c8bf061"

        product_id = ProductIDBuilder().set_uuid(id).build()
        new_session = (
            ProductSessionBuilder()
            .set_description("이 오븐은 효율적이고 안전한 방식으로 음식을 구워줍니다.")
            .set_seller_id("82090bfba6d04a84a669c2a97c0ef283")
            .set_name("오븐")
            .set_price(9513)
            .set_key()
            .build()
        )
        self.assertEqual(
            r'{"check_product": true, "check_img": false, "seller_id": "82090bfba6d04a84a669c2a97c0ef283", "name": "오븐", "price": 9513, "description": "이 오븐은 효율적이고 안전한 방식으로 음식을 구워줍니다."}',
            new_session.serialize_value(),
        )

        read_session = (
            ProductSessionBuilder()
            .set_deserialize_key(new_session.get_id())
            .set_deserialize_value(new_session.serialize_value())
            .unwrap()
            .build()
        )
        self.assertEqual(new_session.serialize_value(), read_session.serialize_value())

        read_read_session = (
            ProductSessionBuilder()
            .set_deserialize_key(read_session.get_id())
            .set_deserialize_value(read_session.serialize_value())
            .unwrap()
            .set_img_path("img01.png")
            .unwrap()
            .build()
        )

        self.assertEqual(
            '{"check_product": true, "check_img": true, "seller_id": "82090bfba6d04a84a669c2a97c0ef283", "name": "오븐", "price": 9513, "description": "이 오븐은 효율적이고 안전한 방식으로 음식을 구워줍니다.", "img_path": "img01.png"}',
            read_read_session.serialize_value(),
        )


def main():
    unittest.main()


if __name__ == "__main__":
    main()
