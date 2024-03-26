import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional, List
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
            client_flag=pymysql.constants.CLIENT.MULTI_STATEMENTS,
        )

    def get_padding_name(self, name: str) -> str:
        return f"{self.name_padding}{name}"

    def load_session(self, session_key: str) -> Result[SessionToken, str]:
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
SELECT value, owner_id, create_time, use_count,id
FROM {session_table_name}
WHERE id = %s;
UPDATE {session_table_name} SET use_count = use_count+1 WHERE id = %s;
"""
                # session_key = MemberSessionBuilder().set_key().build()
                cursor.execute(query, (session_key,session_key))

                result = cursor.fetchone()

                if result is None:
                    return Err("세션 데이터가 존재하지 않습니다.")
                

                session_token = SessionToken(
                    value=result[0],
                    owner_id=result[1],
                    create_time=result[2],
                    use_count=result[3],
                    key=result[4],
                )
                connection.commit()

                cursor.close()
                connection.close()

                return Ok(session_token)

        except Exception as e:
            return Err(str(e))
        
    
    def load_session_from_owner_id(self, owner_id: str) -> Result[List[SessionToken], str]:
        
        connection = self.connect()
        session_table_name = self.get_padding_name("session")
        try:
            with connection.cursor() as cursor:
                query = f"""
SELECT value, owner_id, create_time, use_count,id
FROM {session_table_name}
WHERE owner_id = %s;
"""
                cursor.execute(query, (owner_id,))
                results = cursor.fetchall()

                session_tokens = []
                for result in results:
                    session_token = SessionToken(
                        value=result[0],
                        owner_id=result[1],
                        create_time=result[2],
                        use_count=result[3],
                        key=result[4],
                    )
                    session_tokens.append(session_token)

                cursor.close()
                connection.close()

                if session_tokens:
                    return Ok(session_tokens)
                else:
                    return Err("세션 데이터가 존재하지 않습니다.")

        except Exception as e:
            return Err(str(e))
