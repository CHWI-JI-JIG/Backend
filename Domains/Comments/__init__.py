import sys
from pathlib import Path

now_path = Path(__file__).resolve().parent
root_path = now_path.parent

if not (str(root_path) in sys.path):
    sys.path.append(str(root_path))

from Domains.Comments.CommentID import (
    CommentID,
    ICommentIDBuilder,
)
from Domains.Comments.Comment import (
    Comment,
    ICommentBuilder,
)

__all__ = [
    "CommentID",
    "ICommentIDBuilder",
    "Comment",
    "ICommentBuilder",
]
