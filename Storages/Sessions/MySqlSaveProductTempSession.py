import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional
from result import Result, Err, Ok

from Domains.Members import *
from Domains.Sessions import *
from Repositories.Members import *
from Repositories.Sessions import *
from Builders.Members import *
from uuid import UUID


import pymysql

from icecream import ic


class MySqlSaveProductTempSession(ISaveableProductTempSession):
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

    def update_or_save_product_temp_session(
        self, session: ProductTempSession
    ) -> Result[ProductTempSession, str]:
        """
        Read User table. Make MemberSession. Save MemberSession

        Returns:
            Result[MemberSession, str]:
                Ok(member_session): Sucess to Save memberSession
                Err(e) : db Error
        """

        connection = self.connect()
        session_table_name = self.get_padding_name("session")

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    f"SELECT COUNT(*) FROM {session_table_name} WHERE id = %s",
                    (session.serialize_key()),
                )
                count = cursor.fetchone()[0]
                if count > 0:
                    cursor.execute(
                        f"UPDATE {session_table_name} SET value = %s WHERE id = %s",
                        (session.serialize_value(), session.serialize_key()),
                    )
                else:
                    cursor.execute(
                        f"INSERT INTO {session_table_name} (id, value) VALUES (%s, %s)",
                        (session.serialize_key(), session.serialize_value()),
                    )

                connection.commit()
                return Ok(session)

        except Exception as e:
            ic()
            connection.close()
            return Err(str(e))
