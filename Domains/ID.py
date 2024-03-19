from dataclasses import dataclass
from abc import ABCMeta, abstractmethod
from typing import Optional, Self


class ID(metaclass=ABCMeta):
    @abstractmethod
    def get_id(self) -> str: ...
    
    # @abstractmethod
    # def get_seq(self) -> Optional[int]: ...
