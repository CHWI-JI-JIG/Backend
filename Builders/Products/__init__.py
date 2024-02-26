import sys
from pathlib import Path

now_path = Path(__file__).resolve().parent
root_path = now_path.parent.parents

if not (str(root_path) in sys.path):
    sys.path.append(str(root_path))

from Builders.Products.BasicProductBuilder import (
    ProductIDBuilder,
)

__all__ = [
    "ProductIDBuilder",
]
