import __init__
import unittest
import sys

from Domains.Members import *
from Builders.Members import *
from Domains.Sessions import *
from Applications.Members.ExtentionMethod import hashing_passwd

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
        member_id = MemberIDBuilder().set_uuid(id).unwrap().build()
        new_session = (
            MemberSessionBuilder()
            .set_key()
            .set_member_id(id)
            .unwrap()
            .set_role("buyer")
            .set_name("이탁균")
            .build()
        )
        self.assertEqual(
            '{"member_id": "d697b39f733a426f96a13fc40c8bf061", "name": "이탁균", "role": "buyer"}',
            new_session.serialize_value(),
        )

        read_session = (
            MemberSessionBuilder()
            .set_deserialize_key(new_session.get_id())
            .set_deserialize_value(new_session.serialize_value())
            .unwrap()
            .build()
        )
        self.assertEqual(new_session, read_session)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
