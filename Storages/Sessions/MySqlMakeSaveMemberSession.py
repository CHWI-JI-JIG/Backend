import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional
from result import Result, Err, Ok

from Domains.Members import *
from Domains.Sessions import *
from Repositories.Members import *
from Repositories.Sessions import *
from Builders.Members import *
from Repositories.Sessions import IMakeSaveMemberSession
from uuid import UUID

import pymysql

from icecream import ic


class MySqlMakeSaveMemberSession(IMakeSaveMemberSession):
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
            client_flag=pymysql.constants.CLIENT.MULTI_STATEMENTS,
        )

    def get_padding_name(self, name: str) -> str:
        return f"{self.name_padding}{name}"

    def make_and_save_session(self, member_id: MemberID) -> Result[MemberSession, str]:
        """
        Read User table. Make MemberSession. Save MemberSession

        Returns:
            Result[MemberSession, str]:
                Ok(member_session): Sucess to Save memberSession
                Err(e) : db Error
        """

        connection = self.connect()
        member_table_name = self.get_padding_name("user")
        session_table_name = self.get_padding_name("session")

        try:
            with connection.cursor() as cursor:
                query = f"""
SELECT name, role
FROM {member_table_name}
WHERE id = %s
"""
                cursor.execute(query, (member_id.get_id(),))

                result = cursor.fetchone()

                if result is None:
                    return Err("회원정보가 없습니다.")

                name, role = result
                match (
                    MemberSessionBuilder()
                    .set_key()
                    .set_name(name)
                    .set_role(role)
                    .set_member_id(member_id.get_id())
                    .map(lambda b: b.build())
                ):
                    case Ok(ret):
                        # MemberSession
                        serialized_key = ret.serialize_key()
                        serialized_value = ret.serialize_value()
                        session = ret
                    case e:
                        return e

                cursor.execute(
                    f"INSERT INTO {session_table_name} (id, value) VALUES (%s, %s)",
                    (serialized_key, serialized_value),
                )
                connection.commit()

                cursor.close()
                connection.close()

                return Ok(session)

        except Exception as e:
            return Err(str(e))
