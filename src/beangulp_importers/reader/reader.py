from dataclasses import dataclass
from typing import Protocol, Iterable, Mapping


class Reader(Protocol):
    def __call__(self, filepath: str) -> Iterable[Mapping[str, str]]:
        ...

