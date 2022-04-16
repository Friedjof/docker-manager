# Friedjof Noweck
# 2022-04-13 Mi

from modules.model.volumes import *
from modules.model.network import *
from modules.model.environment import *
from modules.model.devices import *


class Image:
    def __init__(self, name: str, version: str = "latest"):
        self.name: str = name
        self.version: str = version

    def getImage(self) -> str:
        return f"{self.name}:{self.version}"


class Service:
    def __init__(
            self, name: str, image: Image,
            volumes: Volumes = None, ports: Ports = None,
            environments: Environments = None,
            networks: Networks = None, devices: Devices = None,
            dns: DNSs = None, restart: str = "always"
    ):
        self.name: str = name
        self.volumes: Volumes = volumes
        self.ports: Ports = ports
        self.environments: Environments = environments
        self.image: Image = image
        self.networks: Networks = networks
        self.devices: Devices = devices
        self.dns: DNSs = dns
        self.restart: str = restart

    def asdict(self) -> dict:
        return {
            "image": self.image.getImage(),
            "container_name": self.name,
            "restart": self.restart,
            "environment": self.environments.astuple(),
            "devices": self.devices.astuple(),
            "volumes": self.volumes.astuple(as_service=True),
            "dns": self.dns.astuple(),
            "networks": self.networks.asdict(as_service=True),
        }


class Services:
    def __init__(self, *servers: Service):
        self.services: Tuple[Service] = servers

    def asdict(self) -> dict:
        return {s.name: s.asdict() for s in self.services}
