import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional
from result import Result, Err, Ok

from Domains.Members import *
from Domains.Sessions import *
from Repositories.Members import *
from Repositories.Sessions import *
from Builders.Members import *
from Repositories.Sessions import ILoadableSession
from uuid import UUID

import pymysql

from icecream import ic


class MySqlLoadSession(ILoadableSession):
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

    def load_session(self, session_key: str) -> Result[str, str]:
        """_summary_

        Args:
            session_key (UUID): session_key is uuid.hex

        Returns:
            Result[str, str]:
                Ok(str) : session value
                Err(str) : str is seasion of error
        """
        connection = self.connect()
        session_table_name = self.get_padding_name("session")
        try:
            with connection.cursor() as cursor:
                query = f"""
SELECT value
FROM {session_table_name}
WHERE id = %s
"""
                # session_key = MemberSessionBuilder().set_key().build()
                cursor.execute(query, (str(session_key),))

                result = cursor.fetchone()

                if result is None:
                    return Err("세션 데이터가 존재하지 않습니다.")

                session_value = result[0]

                # session_builder = MemberSessionBuilder().set_deserialize_key(str(session_key)).set_deserialize_value(session_value)
                # member_session = session_builder.build()

                connection.commit()

                cursor.close()
                connection.close()

                return Ok(session_value)

        except Exception as e:
            return Err(str(e))
