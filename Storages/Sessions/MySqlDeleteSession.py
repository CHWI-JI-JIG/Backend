import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional
from result import Result, Err, Ok

from Domains.Sessions import *
from Repositories.Sessions import *
from Repositories.Sessions import IDeleteableSession
from uuid import UUID

import pymysql

from icecream import ic


class MySqlDeleteSession(IDeleteableSession):
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
    

    def delete_session_to_key(self, session_key: str) -> Result[bool, str]: 
        connection = self.connect()
        session_table_name = self.get_padding_name("session")
        try:
            with connection.cursor() as cursor:
                query = f"""
DELETE FROM {session_table_name}
WHERE id = %s
"""
                cursor.execute(query, (session_key,))
                connection.commit()
                affected_rows = cursor.rowcount  # delete 쿼리에 영향을 받은 행의 수
                cursor.close()
                connection.close()

                if affected_rows > 0:
                    return Ok(True)
                else:
                    return Err("No session found with the provided session key.")

        except Exception as e:
            return Err(str(e))
        
 
        
    def delete_session_to_owner_id(self, owner_id: str) -> Result[bool, str]:
        connection = self.connect()
        session_table_name = self.get_padding_name("session")
        try:
            with connection.cursor() as cursor:
                query = f"""
DELETE FROM {session_table_name}
WHERE owner_id = %s
"""
                cursor.execute(query, (owner_id,))
                connection.commit()
                affected_rows = cursor.rowcount  # delete 쿼리에 영향을 받은 행의 수

                if affected_rows > 0:
                    return Ok(True)
                else:
                    return Err("No session found with the provided owner_id.")

        except Exception as e:
            return Err(str(e))
        
        
    


