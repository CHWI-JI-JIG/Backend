import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional
from result import Result, Err, Ok

from Domains.Members import *
from Domains.Sessions import *
from Repositories.Members import *
from Repositories.Sessions import *
from Builders.Members import *
from Repositories.Sessions import ISaveableOrderTransition
from uuid import UUID

import pymysql

from icecream import ic


class MySqlSaveOrderTransition(ISaveableOrderTransition):
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

    def save_order_transition(
        self, transition: OrderTransitionSession
    ) -> Result[OrderTransitionSession, str]:
        try:
            connection = self.connect()
            session_table_name = self.get_padding_name("session")

            with connection.cursor() as cursor:
                cursor.execute(
                    f"""
INSERT INTO {session_table_name} (
id, value, owner_id, create_time, use_count
) VALUES (%s, %s,%s,%s,0);
""",
                    (
                        transition.serialize_key(),
                        transition.serialize_value(),
                        transition.get_owner_id(),
                        transition.get_create_time(),
                    ),
                )
                connection.commit()

                return Ok(transition)

        except Exception as e:
            connection.close()
            return Err(str(e))

    def update_order_transition(
        self, transition: OrderTransitionSession
    ) -> Result[OrderTransitionSession, str]:
        try:
            connection = self.connect()
            session_table_name = self.get_padding_name("session")

            with connection.cursor() as cursor:
                update_query = f"""
UPDATE {session_table_name} SET value = %s, use_count = use_count+1 WHERE id = %s """

                cursor.execute(
                    update_query,
                    (
                        transition.serialize_value(),
                        transition.serialize_key(),
                    ),
                )

                connection.commit()
                return Ok(transition)

        except Exception as e:
            ic()
            ic(e)
            connection.close()
            return Err(str(e))
