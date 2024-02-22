import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional
from result import Result, Err,Ok
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


    def identify_and_authenticate(self, account: str, passwd: str) -> Result[Authentication, str]:
        
        connection = self.connect()
        user_table_name = self.get_padding_name("user")
        
        try:
            with connection.cursor() as cursor:
                query = f"""
SELECT seq, id, passwd, last_access, fail_count
FROM {user_table_name}
WHERE account = '%s';
                """
                
                cursor.execute(query, (account,)) 
                result = cursor.fetchone()             
            
            if not result:
                return Err("아이디가 존재하지 않습니다. 회원가입을 해주세요.")
            
            
            if result[2] != passwd:
                Fbuilder = AuthenticationBuilder().set_last_access().set_is_sucess(False).set_fail_count(0).set_id(result[1]).build()
                return Ok(Fbuilder)
            
            Tbuilder = AuthenticationBuilder().set_last_access().set_is_sucess(True).set_fail_count(0).set_id(result[1]).build()
            return Ok(Tbuilder)
            
        except Exception as e:
            return Err(str(e))


        
        
    def update_access(self, auth: Authentication) -> Result[None, str]:
        """_summary_
        Update last_access with the current time, and Update the fail_count according to the successes and failures.

        Args:
            auth (Authentication): Use the value returned by identify_and_authenticate as is.

        Returns:
            Result[None, str]:
                Err(str) : Represents errors in storage, if any, as a string.
        """
        raise NotImplementedError()
