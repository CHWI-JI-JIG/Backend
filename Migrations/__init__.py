import sys
from pathlib import Path

now_path = Path(__file__).resolve().parent
root_path = now_path.parent

if not (str(root_path) in sys.path):
    sys.path.append(str(root_path))
    
from Migrations.MySqlCreateOtp import MySqlCreateOtp
from Migrations.MySqlCreateProduct import MySqlCreateProduct
from Migrations.MySqlCreateUser import MySqlCreateUser
from Migrations.MySqlCreateSession import MySqlCreateSession
from Migrations.MySqlCreateComments import MySqlCreateComments
from Migrations.MySqlCreateOrder import MySqlCreateOrder

__all__ = [
    "MySqlCreateOtp",
    "MySqlCreateProduct",
    "MySqlCreateUser",
    "MySqlCreateSession",
    "MySqlCreateOrder",
    "MySqlCreateComments",
]
