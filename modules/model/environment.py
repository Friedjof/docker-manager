# Friedjof Noweck
# 2022-04-13 Mi

from __future__ import annotations

from typing import Tuple


class Environment:
    def __init__(self, key: str, value: str | int | bool):
        self.key: str = key
        self.value: str | int | bool = value

    def asdict(self) -> dict:
        return {self.key: self.value}


class Environments:
    def __init__(self, *environments: Environment):
        self.environments: Tuple[Environment] = environments

    def astuple(self) -> Tuple:
        return tuple([e.asdict() for e in self.environments])
