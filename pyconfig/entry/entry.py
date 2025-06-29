from abc import ABC, abstractmethod
from io import IOBase


class Entry(ABC):
    def __init__(self, file: IOBase):
        self.file = file

    @abstractmethod
    def get(self, path: str):
        pass
