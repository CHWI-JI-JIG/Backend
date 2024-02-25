import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional
from result import Result, Err, Ok

from Domains.Members import *
from Domains.Sessions import *
from Repositories.Members import *
from Repositories.Sessions import *
from Builders.Members import *
from Repositories.Sessions import IUseableSession
from uuid import UUID

import pymysql

from icecream import ic


class MySqlSaveSession(IUseableSession):
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

    @abstractmethod
    def save_session(self, session: ISessionSerializeable) -> Result[UUID, str]:
        """_summary_

        Args:
            session (ISesseionSerializeable):

        Returns:
            Result[None, str]:
                Ok(UUID): Seccess
                Err(str): str is reason of error
        """
        session.serialize_key()
        session.serialize_value()
    
        connection = self.connect()
        session_table_name = self.get_padding_name("session")
        try:
            # 커서 생성
            with connection.cursor() as cursor:
                insert_query = f"""
INSERT INTO {session_table_name} (
    key,
    value
) VALUES (%s, %s);
                """
                cursor.execute(
                    insert_query,
                    (
                        session.get_id(),
                        session.serialize_key,
                        session.serialize_value,                        
                    ),
                )
                # 변경 사항을 커밋
                connection.commit()
                return Ok(session.key)
        except Exception as e:
            connection.rollback()
            connection.close()
            return Err(str(e))
        
    # def load_session(self, session_key: str) -> Result[str, str]:
        """_summary_

        Args:
            session_key (UUID): session_key is uuid.hex

        Returns:
            Result[str, str]:
                Ok(str) : session value
                Err(str) : str is seasion of error
        """
        ...
        ## value 값 해석할필요 없다. 