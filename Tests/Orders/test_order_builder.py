import __init__
import unittest
import sys

from Domains.Members import *
from Builders.Members import *
from Builders.Products import *
from Domains.Sessions import *
from Applications.Members.ExtentionMethod import hashing_passwd

from icecream import ic


class test_order_builder(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = "test"
        print(sys._getframe(0).f_code.co_name, f"(test_order_builder)")

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

    def test_order_transition_생성후_이후_성공_추가(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t\t", sys._getframe(0).f_code.co_name)
        id = "d697b39f733a426f96a13fc40c8bf061"
        uid = "365b77a0a6b34fe28c7112d6c1bb64ca"
        product_id = ProductIDBuilder().set_uuid(id).build()
        new_order_transition = (
            OrderTransitionBuilder()
            .set_key()
            .set_buyer_id(uid)
            .set_recipient_name("test name")
            .set_recipient_phone("01033458312")
            .set_recipient_address("guri suteak")
            .set_product_id(id)
            .set_count_and_price(3, 2000)
            .build()
        )

        self.assertEqual(
            '{"check_success": false, "buyer_id": "365b77a0a6b34fe28c7112d6c1bb64ca", "recipient_name": "test name", "recipient_phone": "01033458312", "recipient_address": "guri suteak", "product_id": "d697b39f733a426f96a13fc40c8bf061", "buy_count": 3, "total_price": 6000}',
            new_order_transition.serialize_value(),
        )

        read_session = (
            OrderTransitionBuilder()
            .set_deserialize_key(new_order_transition.get_id())
            .set_deserialize_value(new_order_transition.serialize_value())
            .unwrap()
            .build()
        )
        self.assertEqual(new_order_transition.key, read_session.key)
        self.assertEqual(
            new_order_transition.order.product_id, read_session.order.product_id
        )
        self.assertEqual(
            new_order_transition.order.buyer_id, read_session.order.buyer_id
        )
        self.assertEqual(
            new_order_transition.order.recipient_name, read_session.order.recipient_name
        )
        self.assertEqual(
            new_order_transition.order.recipient_address,
            read_session.order.recipient_address,
        )
        self.assertEqual(
            new_order_transition.order.recipient_phone,
            read_session.order.recipient_phone,
        )
        self.assertEqual(
            new_order_transition.order.buy_count, read_session.order.buy_count
        )
        self.assertEqual(
            new_order_transition.order.total_price, read_session.order.total_price
        )
        self.assertIsNone(read_session.is_success)

        success_session = (
            OrderTransitionBuilder()
            .set_deserialize_key(read_session.get_id())
            .set_deserialize_value(read_session.serialize_value())
            .unwrap()
            .set_is_success(True)
            .build()
        )

        self.assertEqual(new_order_transition.key, success_session.key)
        self.assertEqual(
            new_order_transition.order.product_id, success_session.order.product_id
        )
        self.assertEqual(
            new_order_transition.order.buyer_id, success_session.order.buyer_id
        )
        self.assertEqual(
            new_order_transition.order.recipient_name,
            success_session.order.recipient_name,
        )
        self.assertEqual(
            new_order_transition.order.recipient_address,
            success_session.order.recipient_address,
        )
        self.assertEqual(
            new_order_transition.order.recipient_phone,
            success_session.order.recipient_phone,
        )
        self.assertEqual(
            new_order_transition.order.buy_count, success_session.order.buy_count
        )
        self.assertEqual(
            new_order_transition.order.total_price, success_session.order.total_price
        )
        self.assertEqual(success_session.is_success, True)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
