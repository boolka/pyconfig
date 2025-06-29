from io import IOBase
from json import load

from .entry import Entry


class JsonEntry(Entry):
    def __init__(self, file: IOBase):
        super().__init__(file)
        self.data = load(file)

    def get(self, path: str):
        data = self.data

        for p in path.split("."):
            if p not in data:
                return None

            try:
                data = data[p]
            except Exception:
                return None

        return data
