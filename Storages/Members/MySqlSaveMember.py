import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional
from result import Result, Err, Ok

from Domains.Members import *
from Repositories.Members import *
from Builders.Members import *
from uuid import UUID

import pymysql
from datetime import datetime

from icecream import ic


class MySqlSaveMember(ISaveableMember):
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

    def save_member(self, member: Member, privacy: Privacy) -> Result[MemberID, str]:
        connection = self.connect()
        user_table_name = self.get_padding_name("user")
        member.id.get_id()
        try:
            # 커서 생성
            with connection.cursor() as cursor:
                insert_query = f"""
INSERT INTO {user_table_name} (
    id,
    account,
    pay_account,
    passwd,
    email,
    role,
    company_registration_number,
    phone,
    address,
    name,
    last_access,
    fail_count
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 0);
                """
                cursor.execute(
                    insert_query,
                    (
                        member.id.get_id(),
                        member.account,
                        privacy.pay_account,
                        member.passwd,
                        privacy.email,
                        str(member.role),
                        privacy.company_registration_number,
                        privacy.phone,
                        privacy.address,
                        privacy.name,
                        datetime.now(),
                    ),
                )
                # 변경 사항을 커밋
                connection.commit()
                return Ok(member.id)
        except Exception as e:
            connection.rollback()
            connection.close()
            return Err(str(e))
