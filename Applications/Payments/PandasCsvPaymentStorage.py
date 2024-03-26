import __init__
from dataclasses import dataclass
from typing import Optional, Tuple, List
from result import Result, Ok, Err
from uuid import UUID

from dataclasses import asdict
from datetime import datetime
from icecream import ic
import pandas as pd
from csv import DictWriter
import pymysql

from Applications.Payments import PayData
from Applications.Payments import IPaymentRepo

@dataclass(frozen=True)
class User:
    id:str
    name:str

class PandasCsvPaymentStorage(IPaymentRepo):
    dict_header = [
        "id",
        "seller_bank_account",
        "seller_id",
        "seller_name",
        "buyer_card_account",
        "buyer_id",
        "buyer_name",
        "transfer_time",
        "withdrawal",
        "deposit",
    ]

    def __init__(self, name_padding: str = "log_"):
        self.name_padding = name_padding
        self.timestamp = datetime.now().strftime("%Y%m%d")

        # 데이터 로드
        file_path = self.get_padding_name(f"{self.timestamp}_payment_data.csv")
        self.file_path = file_path
        try:
            self.df: pd.DataFrame = pd.read_csv(file_path)
        except FileNotFoundError:
            self.df: pd.DataFrame = pd.DataFrame(columns=self.dict_header)
        except:
            assert False, "load error"

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

    # def load_id

    def save_pay_data(self, data: PayData) -> Result[PayData, str]:
        # 기존 데이터 로드
        file_path = self.file_path

        # data를 dict으로 변경
        new_row = asdict(data)
        # self.df에 새로운 데이터 추가
        self.df.loc[len(self.df)] = new_row

        # CSV 파일로 저장
        self.df.to_csv(file_path, index=False)

        return Ok(data)

    def load_pay_data(self, id: UUID) -> Optional[PayData]:
        # ID로 데이터 검색
        data_row = self.df.loc[self.df["id"] == id.hex].to_dict(orient="records")

        if not data_row:
            return None

        return PayData(**data_row[0])

    def load_list_of_pay_data(
        self,
        seller_name: Optional[str] = None,
        buyer_name: Optional[str] = None,
        page=0,
        size=10,
    ) -> Result[Tuple[int, List[PayData]], str]:
        # 필터링
        if seller_name:
            self.df = self.df.loc[self.df["seller_name"] == seller_name]
        if buyer_name:
            self.df = self.df.loc[self.df["buyer_name"] == buyer_name]

        total_rows = len(self.df)
        start_idx = page * size
        end_idx = start_idx + size

        # 페이지에 맞게 잘라내기
        page_data = self.df.iloc[start_idx:end_idx].to_dict(orient="records")

        return Ok((total_rows, [PayData(**row) for row in page_data]))
