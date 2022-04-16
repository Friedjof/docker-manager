# Friedjof Noweck
# 2022-04-13 Mi

from __future__ import annotations

from typing import Tuple
from pathlib import Path


class VDriverOption:
    def __init__(self, key: str, value: str | int | bool):
        self.key: str = key
        self.value: str | int | bool = value

    def asdict(self) -> dict:
        return {self.key: self.value}


class VDriverOptions:
    def __init__(self, *options: VDriverOption):
        self.options: Tuple[VDriverOption] = options

    def append(self, option: VDriverOption) -> None:
        self.options: Tuple[VDriverOption] = tuple(set(self.options + (option,)))

    def asdict(self) -> dict:
        return {o.key: o.value for o in self.options}


class VDriver:
    def __init__(self, name: str):
        self.name: str = name


class Volume:
    def __init__(
            self, name: str, container: Path, host: Path = None,
            driver: VDriver = None, driver_options: VDriverOptions = None,
            external: bool = False
    ):
        self.name: str = name
        self.host: Path = host
        self.container: Path = container
        self.external: bool = external
        self.driver: VDriver = driver
        self.driver_options: VDriverOptions = driver_options
        self.driver_options.append(VDriverOption("device", f"{self.host}"))

    def asDict(self) -> dict:
        return {self.name: {"driver": self.driver.name, "driver_opts": self.driver_options.asdict()}}


class Volumes:
    def __init__(self, *volumes: Volume):
        self.volumes: Tuple[Volume] = volumes

    def astuple(self, as_service: bool = False) -> Tuple:
        if as_service:
            return tuple([f"{v.name}:{v.container}" for v in self.volumes])
        else:
            return tuple([v.asDict() for v in self.volumes])

    def asdict(self) -> dict:
        return {v.name: v.asDict() for v in self.volumes}
