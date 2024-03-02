from dataclasses import dataclass
from abc import ABCMeta, abstractmethod
from typing import Optional, Self
from uuid import uuid4, UUID


class ID(metaclass=ABCMeta):
    @abstractmethod
    def get_id(self) -> str: ...
