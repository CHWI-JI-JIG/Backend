import __init__
from abc import ABCMeta, abstractmethod
from typing import Self


class ISessionSerializeable(metaclass=ABCMeta):
    @abstractmethod
    def serialize_key(self) -> str: ...

    @abstractmethod
    def serialize_value(self) -> str: ...


class ISesseionBuilder(metaclass=ABCMeta):
    @abstractmethod
    def set_deserialize_key(self, key: str) -> Self: ...

    @abstractmethod
    def set_deserialize_value(self, value: str) -> Self: ...
