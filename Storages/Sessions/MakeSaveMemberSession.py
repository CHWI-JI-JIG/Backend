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


class MakeSaveMemberSession(IUseableSession):
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
    def make_and_save_session(self,member_id:MemberID) -> Result[MemberSession, str]:
        """
        Read User table. Make MemberSession. Save MemberSession

        Returns:
            Result[MemberSession, str]:
                Ok(member_session): Sucess to Save memberSession
                Err(e) : db Error
        """
        
        # 멤버 ID로부터 이름과 역할 데이터 가져오기
        # 예: member_id로부터 이름을 가져오는 코드
        name = "example_name"

        # 예: member_id로부터 역할을 가져오는 코드
        role = "example_role"

        # MemberSession 생성
        session = MemberSessionBuilder().set_key().set_member_id(str(member_id)).set_name(name).set_role(role).build()

        # Serialize key 및 value 생성
        serialized_key = session.serialize_key()
        serialized_value = session.serialize_value()

        # 데이터베이스에 세션 저장
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute(
                f"INSERT INTO log_session (session_key, session_value) VALUES (%s, %s)",
                (serialized_key, serialized_value),
            )
            conn.commit()
            cursor.close()
            conn.close()
            return Ok(session)
        
        except pymysql.MySQLError as e:
            return Err(str(e))
