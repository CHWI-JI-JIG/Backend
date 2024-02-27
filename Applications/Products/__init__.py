import sys
from pathlib import Path

now_path = Path(__file__).resolve().parent
root_path = now_path.parent.parents

if not (str(root_path) in sys.path):
    sys.path.append(str(root_path))

from Applications.Products.CreateProductService import CreateProductService
from Applications.Products.ReadProductService import ReadProductService

__all__ = [
    "CreateProductService",
    "ReadProductService",
]
