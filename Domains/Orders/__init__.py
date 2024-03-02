import sys
from pathlib import Path

now_path = Path(__file__).resolve().parent
root_path = now_path.parent

if not (str(root_path) in sys.path):
    sys.path.append(str(root_path))

from Domains.Orders.OrderID import (
    OrderID,
    IOrderIDBuilder,
)
from Domains.Orders.Order import (
    Order,
    IOrderBuilder,
)

__all__ = [
    "OrderID",
    "IOrderIDBuilder",
    "Order",
    "IOrderBuilder",
]
