import sys
from pathlib import Path

now_path = Path(__file__).resolve().parent
root_path = now_path.parent.parents

if not (str(root_path) in sys.path):
    sys.path.append(str(root_path))

from Applications.Comments.CreateCommentService import CreateCommentService
from Applications.Comments.ReadCommentService import ReadOrderService

__all__ = [
    "CreateCommentService",
    "ReadOrderService",
]
