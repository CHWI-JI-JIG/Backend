import sys
from pathlib import Path

now_path = Path(__file__).resolve().parent
root_path = now_path.parent

if not (str(root_path) in sys.path):
    sys.path.append(str(root_path))

from Domains.ID import ID, IDBuilder

__all__ = [
    "ID",
    "IDBuilder",
]
