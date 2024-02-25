import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional
from result import Result, Err, Ok

from Domains.Members import *
from Repositories.Members import *
from Builders.Members import *
from uuid import UUID

import pymysql

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
        )

    def get_padding_name(self, name: str) -> str:
        return f"{self.name_padding}{name}"

    def save_product(self):
        connection = self.connect()
        user_table_name = self.get_padding_name("product")
        member.id.get_id()
        try:
            # 커서 생성
            with connection.cursor() as cursor:
                insert_query = f"""
INSERT INTO {user_table_name} (
    id,
    name,
    last_access,
    fail_count
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
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
                        builder.str_last_access(),
                        0,
                    ),
                )
                # 변경 사항을 커밋
                connection.commit()
                return Ok(member.id.uuid)
        except Exception as e:
            connection.rollback()
            connection.close()
            return Err(str(e))
