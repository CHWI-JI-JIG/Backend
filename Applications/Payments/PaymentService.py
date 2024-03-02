import __init__
from typing import Optional
from dataclasses import dataclass
from result import Result, Ok, Err

from Domains.Members import *
from Domains.Products import *
from Domains.Orders import *
from Domains.Sessions import *
from Builders.Members import *

from Repositories.Members import *
from Repositories.Products import *
from Repositories.Orders import *
from Repositories.Products import *
from Repositories.Sessions import *

from icecream import ic
from datetime import datetime
from uuid import UUID, uuid4

from Domains.Sessions import *
from Applications.Payments import IPaymentRepo, PandasCsvPaymentStorage, PayData
from Storages.Sessions import *
from get_config_data import get_db_padding


@dataclass(frozen=True)
class Card:
    account: str
    balance: int


@dataclass
class Bank:
    account: str
    balance: int


class PaymentService:
    cards = [
        Card(account="1111-1111-1111-1111", balance=500000),
        Card(account="2222-2222-2222-2222", balance=500000),
    ]
    banks = [
        Bank(account="1231-1231-1231-1231", balance=100000),
    ]

    def __init__(
        self,
    ):
        self.pay_repo = PandasCsvPaymentStorage(get_db_padding())
        self.load_repo = MySqlLoadSession(get_db_padding())

    def approval_and_logging(
        self,
        transition_key: str,
        total_price: int,
        card_account: str,
        bank_account: str = "1231-1231-1231-1231",
    ) -> Result[bool, str]:
        """
        1. 카드번호 유효성, 통장 유효성 확인
        2. 입/출금이 되는지 확인
        3. 해당 카드번호에서 인출해서 통장으로 입금
        4. 위에 내용 pay_repo에 저장
        """
        assert isinstance(total_price, int), "Type of total_price is int."
        # 1. 카드번호 및 통장번호 유효성 확인
        card = next((c for c in self.cards if c.account == card_account), None)
        bank = next((b for b in self.banks if b.account == bank_account), None)

        if not card:
            return Err("Invalid card number")
        if not bank:
            return Err("Invalid bank account")
        assert isinstance(bank, Bank), "Type of bank is Bank"
        assert isinstance(card, Card), "Type of card is Card"

        # 2. 출금이 가능한지 확인
        if card.balance < total_price:
            return Err("Insufficient funds in the card")

        # 3. 인출 및 입금
        # card.balance -= total_price
        # bank.balance += total_price

        # 4. 위에 내용 pay_repo에 저장
        pay_data = PayData(
            id=str(uuid4()),
            seller_bank_account=bank_account,
            seller_id="ss",
            seller_name="name",
            buyer_card_account=card_account,
            buyer_id="id",
            buyer_name="namename",
            withdrawal=-total_price,
            deposit=total_price,
            transfer_time=datetime.now(),
        )

        result = self.pay_repo.save_pay_data(pay_data)

        if result.is_err():
            return Err(result.err())
        return Ok(True)
