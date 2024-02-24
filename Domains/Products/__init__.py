import sys
from pathlib import Path

now_path = Path(__file__).resolve().parent
root_path = now_path.parent

if not (str(root_path) in sys.path):
    sys.path.append(str(root_path))

from Domains.Products.ProductID import (
    ProductID,
    IProductIDBuilder,
)
from Domains.Products.Product import (
    Product,
    IProductBuilder,
)

__all__ = [
    "ProductID",
    "IProductIDBuilder",
    "Product",
    "IProductBuilder",
]
