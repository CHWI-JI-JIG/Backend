import sys
from pathlib import Path

now_path = Path(__file__).resolve().parent
root_path = now_path.parent.parent

if not (str(root_path) in sys.path):
    sys.path.append(str(root_path))

from Repositories.Products.ISaveableProduct import ISaveableProduct
from Repositories.Products.IGetableProduct import IGetableProduct

__all__ = [
    "ISaveableProduct",
    "IGetableProduct",
]
