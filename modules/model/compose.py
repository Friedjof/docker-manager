# Friedjof Noweck
# 2022-04-13 Mi

from __future__ import annotations
from collections import Set

from modules.model.services import *


class Compose:
    def __init__(self, services: Services, version: float | int):
        self.services: Services = services
        self.version: float | int = version

        all_networks: Set[Network] = set()
        all_volumes: Set[Volume] = set()

        for s in self.services.services:
            for n in s.networks.networks:
                all_networks.add(n)
            for v in s.volumes.volumes:
                all_volumes.add(v)

        self.networks: Networks = Networks(*all_networks)
        self.volumes: Volumes = Volumes(*all_volumes)

    def asdict(self) -> dict:
        return {
            "version": f'{self.version}',
            "services": self.services.asdict(),
            "networks": self.networks.asdict(),
            "volumes": self.volumes.asdict()
        }
