import sys
from pathlib import Path

now_path = Path(__file__).resolve().parent
root_path = now_path.parent.parent

if not (str(root_path) in sys.path):
    sys.path.append(str(root_path))

from Storages.Products.MySqlSaveProduct import MySqlSaveProduct
from Storages.Products.MySqlGetProduct import MySqlGetProduct

__all__=[
    "MySqlSaveProduct",
    "MySqlGetProduct",
]