# Friedjof Noweck
# 2022-04-13 Mi

from typing import Tuple
from pathlib import Path


class Device:
    def __init__(self, path: Path):
        self.path: Path = path


class Devices:
    def __init__(self, *devices: Device):
        self.devices: Tuple[Device] = devices

    def astuple(self) -> Tuple:
        return tuple([f"{d.path}" for d in self.devices])
