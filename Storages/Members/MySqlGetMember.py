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


class MySqlGetMember(IReadableMemberList):
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

    def get_members(
        self,
        page=0,
        size=10,
    ) -> Result[Tuple[int, List[Member]], str]:
        
        connection = self.connect()
        user_table_name = self.get_padding_name("user")
        #여기부터 수정 중
        try:
            # 커서 생성
            with connection.cursor() as cursor:
                offset = page * size
                query = f"""
SELECT id, account, role
FROM {user_table_name}
ORDER BY seq DESC
LIMIT %s, %s
"""                
                cursor.execute(query, (offset, size))
                result = cursor.fetchall()

                users = []
                for row in result:
                    id, account, role = row
                    member = Member(
                        id=MemberIDBuilder().set_uuid(id).build(),
                        account=account,  # Member 클래스에 account 인자가 있는지 확인
                        role=role
                    )
                    users.append(member)

                cursor.execute(f"SELECT COUNT(*) FROM {user_table_name}")
                total_count = cursor.fetchone()[0]

                connection.commit()

                return Ok((total_count, users))
            # 여기 아래로 수정 안해도됨
        except Exception as e:
            print(e)
            connection.close()  
            return Err(str(e)) 