import __init__

from result import Result, Err, Ok

from Domains.Members import *
from Repositories.Members import *
from Builders.Members import *


import pymysql

class MySqlEditMember(IEditableMember): 
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
    
    def update_member(self, member: Member) -> Result[MemberID, str]:
        connection = self.connect()
        user_table_name = self.get_padding_name("user")
        member.id.get_id()
        try:
            # 커서 생성
            with connection.cursor() as cursor:
                update_query = f"""
UPDATE {user_table_name} 
SET role = %s
WHERE id= %s
                """
                cursor.execute(
                    update_query,
                    (
                        str(member.role),
                        member.id.get_id()
                    ),
                )
                # 변경 사항을 커밋
                connection.commit()
                return Ok(member.id)
        except Exception as e:
            connection.rollback()
            connection.close()
            return Err(str(e))
    
    