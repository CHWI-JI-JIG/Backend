import sys
from pathlib import Path

now_path = Path(__file__).resolve().parent
root_path = now_path.parent

if not (str(root_path) in sys.path):
    sys.path.append(str(root_path))

from Migrations.MySqlCreateProduct import MySqlCreateProduct
from Migrations.MySqlCreateUser import MySqlCreateUser
from Migrations.MySqlCreateSession import MySqlCreateSession

__all__ = [
    "MySqlCreateProduct",
    "MySqlCreateUser",
    "MySqlCreateSession",
]
