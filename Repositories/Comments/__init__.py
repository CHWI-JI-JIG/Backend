import sys
from pathlib import Path

now_path = Path(__file__).resolve().parent
root_path = now_path.parent.parent

if not (str(root_path) in sys.path):
    sys.path.append(str(root_path))

from Repositories.Comments.ISaveableComment import ISaveableComment
from Repositories.Comments.IGetableComment import IGetableComment

__all__ = [
    "ISaveableComment",
    "IGetableComment",
    "IReadableComment",
]
