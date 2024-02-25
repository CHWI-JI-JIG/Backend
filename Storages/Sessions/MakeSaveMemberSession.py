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


class MakeSaveMemberSession(IMakeSaveMemberSession):
    def __init__(self, name_padding: str = "test_makesave_"):
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
    def make_and_save_session(self,member_id:MemberID) -> Result[MemberSession, str]:
        """
        Read User table. Make MemberSession. Save MemberSession

        Returns:
            Result[MemberSession, str]:
                Ok(member_session): Sucess to Save memberSession
                Err(e) : db Error
        """

        connection = self.connect()
        member_table_name = self.get_padding_name("member")
        session_table_name = self.get_padding_name("session")
        
        try:
            with connection.cursor() as cursor:
                select_query = f"""
SELECT name, role
FROM {member_table_name}
WHERE id = %s
"""
                cursor.execute(
                    select_query,
                    (str(member_id),)
                )
            
                result = cursor.fetchone()
            
                if result is None:
                    return Err("회원정보가 없습니다.")
                
                name, role = result
                session = MemberSessionBuilder().set_key().set_member_id(str(member_id)).set_name(name).set_role(role).build()
                
                # MemberSession
                serialized_key = session.serialize_key()
                serialized_value = session.serialize_value()

                insert_query = f"""
INSERT INTO {session_table_name} (
    id,
    value
) VALUES (%s, %s);
"""
            
                cursor.execute(
                    insert_query,
                    (serialized_key, serialized_value)
                )
                connection.commit()
                
                cursor.close()
                connection.close()
                
                return Ok(session)
        
        except Exception as e:
            return Err(str(e))
