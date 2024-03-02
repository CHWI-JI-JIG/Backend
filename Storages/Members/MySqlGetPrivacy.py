from Repositories.Members.IReadableMemberList import IReadableMemberList
import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional, Tuple, List
from result import Result, Err, Ok

from Domains.Members import *
from Repositories.Members import *
from Builders.Members import *
from uuid import UUID

import pymysql

from icecream import ic


class MySqlGetPrivacy(IReadableMember):
    def __init__(self, name_padding: str = "log_"):
        self.name_padding = name_padding

    def connect(self):
        from get_config_data import get_mysql_dict

        sql_config = get_mysql_dict()
        return pymysql.connect(
            host=sql_config["host"],
            user=sql_config["user"],
            password=sql_config["password"],
            db=sql_config["database"],
            charset=sql_config["charset"],
        )

    def get_padding_name(self, name: str) -> str:
        return f"{self.name_padding}{name}"

    def get_privacy(self, member_id: MemberID) -> Result[Privacy, str]:

        connection = self.connect()
        user_table_name = self.get_padding_name("user")

        try:

            with connection.cursor() as cursor:

                query = f"""
                    SELECT id, name, phone, email, address, pay_account, company_registration_number
                    FROM {user_table_name}
                    WHERE id = %s
                """
                cursor.execute(query, (member_id.get_id(),))

                result = cursor.fetchone()

                if not result:
                    return Err("Member not found")

                (
                    id,
                    name,
                    phone,
                    email,
                    address,
                    pay_account,
                    company_registration_number,
                ) = result

                privacy = Privacy(
                    id=member_id,
                    name=name,
                    phone=phone,
                    email=email,
                    address=address,
                    pay_account=pay_account,
                    company_registration_number=company_registration_number,
                )

                connection.commit()

                return Ok(privacy)

        except Exception as e:
            print(e)
            connection.rollback()
            return Err(str(e))

        finally:
            connection.close()
