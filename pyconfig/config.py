from dataclasses import dataclass
from os import listdir, path
from socket import gethostname

from os import environ
from .source import parse_filename, EntrySource
from .entry.entry import Entry
from .entry.toml import TomlEntry
from .entry.json import JsonEntry


@dataclass
class Source:
    filename: str
    source: EntrySource
    deployment: str | None
    instance: int | None
    entry: Entry


class Config:
    def __init__(
        self,
        directory: str,
        deployment: str | None = None,
        instance: int | None = None,
        hostname: str | None = None,
    ):
        self.directory = directory
        self.deployment = deployment
        self.instance = instance
        self.hostname = hostname or gethostname()

        self.sources: list[Source] = []

    def init(self):
        for filename in listdir(self.directory):
            entry: Entry
            file, ext = path.splitext(filename)
            src, dep, inst = parse_filename(path.basename(file), self.hostname)

            with open(path.join(self.directory, filename), "rb") as f:
                match ext:
                    case ".toml":
                        entry = TomlEntry(f)
                    case ".json":
                        entry = JsonEntry(f)
                    case _:
                        continue

            self.sources.append(
                Source(
                    filename,
                    src,
                    dep,
                    inst,
                    entry,
                )
            )

        self.sources.sort(key=lambda s: s.source)
        self.sources.reverse()

    def get(self, path: str):
        for src in self.sources:
            data = src.entry.get(path)

            if data is not None:
                if src.source == EntrySource.env_src:
                    data = environ[data]

                return data

        return None
