# Friedjof Noweck
# 2022-04-13 Mi

from __future__ import annotations
from typing import Tuple, List

from ipaddress import IPv4Network, IPv4Address, IPv6Address, IPv6Network

from modules.datatypes import Unsigned16BitInt


class IPv4Gateway(IPv4Address):
    def __init__(self, address: object):
        super().__init__(address)


class IPv6Gateway(IPv6Address):
    def __init__(self, address: object):
        super().__init__(address)


class Option:
    def __init__(self, key: str, value: str | int | bool):
        self.key: str = key
        self.value: str | int | bool = value

    def asdict(self) -> dict:
        return {self.key: self.value}


class Options:
    def __init__(self, *options: Option):
        self.options: Tuple[Option] = options

    def asdict(self) -> dict:
        return {o.key: o.value for o in self.options}


class IpamConfig:
    def __init__(self, network: IPv4Network | IPv6Network, gateway: IPv4Gateway | IPv6Gateway = None):
        self.network: IPv4Network | IPv6Network = network
        self.gateway: IPv4Gateway | IPv6Gateway = gateway

    def is_valid(self) -> bool:
        return self.gateway in self.network and\
               self.gateway != self.network.broadcast_address and\
               self.gateway != self.network.network_address

    def astuple(self) -> Tuple:
        result: List = [{"subnet": self.network.with_prefixlen}]
        if self.gateway:
            result.append({"gateway": self.gateway})

        return tuple(result)


class Driver:
    def __init__(self, name: str = "default", options: Options = None):
        self.name: str = name
        self.options: Options = options

    def asdict(self) -> dict:
        if self.options:
            return {"name": self.name, "options": self.options}
        else:
            return {"name": self.name}


class Ipam:
    def __init__(self, driver: Driver, config: IpamConfig):
        self.driver: Driver = driver
        self.config: IpamConfig = config

    def asdict(self) -> dict:
        return {"driver": f'"{self.driver.name}"', "config": self.config.astuple()}


class Port:
    def __init__(self, host: int, container: int):
        self.host: Unsigned16BitInt = Unsigned16BitInt(host)
        self.container: Unsigned16BitInt = Unsigned16BitInt(container)

    def asdict(self) -> dict:
        return {"host": self.host, "container": self.container}


class Ports:
    def __init__(self, *ports: Port):
        self.ports: Tuple[Port] = ports


class Network:
    def __init__(
            self, name: str, driver: Driver, ipam: Ipam
    ):
        self.name: str = name
        self.driver: Driver = driver
        self.ipam: Ipam = ipam
        self.subnet: IPv4Network | IPv6Network = self.ipam.config.network

    def asdict(self) -> dict:
        return {
                "driver": self.driver.name,
                "driver_opts": None if not self.driver.options else self.driver.options.asdict(),
                "ipam": {
                    "driver": self.ipam.driver.asdict(),
                    "config": self.ipam.config.astuple()
                }
            }


class ContainerNetwork:
    def __init__(self, network: Network, ip: IPv4Address | IPv6Address):
        self.network: Network = network
        self.ip: IPv4Address | IPv6Address = ip

        self.IPv4: bool = type(self.ip) is IPv4Address

    def is_valid(self) -> bool:
        return self.ip in self.network and\
               self.ip is not self.network.ipam.config.network.broadcast_address and\
               self.ip is not self.network.ipam.config.network.network_address and\
               self.ip is not self.network.ipam.config.gateway


class Networks:
    def __init__(self, *networks: ContainerNetwork):
        self.networks: Tuple[ContainerNetwork] = networks

    def asdict(self, as_service: bool = False) -> dict:
        if as_service:
            result: dict = {}
            for n in self.networks:
                if n.IPv4:
                    result[n.network.name] = {"ipv4_address": f"{n.ip}"}
                else:
                    result[n.network.name] = {"ipv6_address": f"{n.ip}"}
            return result
        else:
            return {n.network.name: n.network.asdict() for n in self.networks}


class DNS:
    def __init__(self, ip: IPv4Address | IPv6Address):
        self.ip: IPv4Address | IPv6Address = ip


class DNSs:
    def __init__(self, *dnss: DNS):
        self.dnss: Tuple[DNS] = dnss

    def astuple(self) -> Tuple:
        return tuple([f"{d.ip}" for d in self.dnss])
