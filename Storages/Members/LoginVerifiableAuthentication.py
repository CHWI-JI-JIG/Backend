import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional
from result import Result, Err, Ok
from datetime import datetime

from Domains.Members import *
from Repositories.Members import *
from Builders.Members import *

import pymysql

from icecream import ic


class LoginVerifiableAuthentication(IVerifiableAuthentication):
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

    def identify_and_authenticate(
        self, account: str, passwd: str
    ) -> Result[Authentication, str]:

        connection = self.connect()
        user_table_name = self.get_padding_name("user")

        try:
            with connection.cursor() as cursor:
                query = f"""
SELECT seq, id, passwd, last_access, fail_count
FROM {user_table_name}
WHERE account = %s;
                """
                cursor.execute(query, (account,))
                result = cursor.fetchone()

            if not result:
                return Err("아이디가 존재하지 않습니다. 회원가입을 해주세요.")
            id = MemberIDBuilder().set_uuid(result[1]).set_seqence(1).build()
            b = (
                AuthenticationBuilder()
                .set_last_access(result[3])
                .set_fail_count(result[4])
                .set_id(id)
            )
            if result[2] != passwd:
                b.set_is_sucess(False)
                return Ok(b.build())
            b.set_is_sucess(True)
            return Ok(b.build())

        except Exception as e:
            return Err(str(e))

    def update_access(self, auth: Authentication) -> Result[None, str]:
        connection = self.connect()
        user_table_name = self.get_padding_name("user")

        try:
            with connection.cursor() as cursor:
                if auth.is_sucess:
                    # 로그인 성공 시 fail_count를 0으로 초기화
                    query = f"""
UPDATE {user_table_name}
SET last_access = %s, fail_count = 0
WHERE id = %s;
                """
                    cursor.execute(query, (datetime.now(), auth.id.get_id()))
                else:
                    # 로그인 실패 시 fail_count를 1 증가
                    query = f"""
UPDATE {user_table_name}
SET last_access = %s, fail_count = fail_count +1
WHERE id = %s;
                """
                    cursor.execute(query, (datetime.now(), auth.id.get_id()))

                connection.commit()

            return Ok(None)

        except Exception as e:
            return Err(str(e))

        finally:
            connection.close()
