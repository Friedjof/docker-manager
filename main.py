# Friedjof Noweck
# 2022-04-13 Mi

import yaml

from modules.model.compose import *


bshome: Network = Network(
    name="bshome",
    driver=Driver(
        name="macvlan",
        options=Options(Option("parent", "eth0"))
    ),
    ipam=Ipam(
        driver=Driver(),
        config=IpamConfig(
            network=IPv4Network("192.168.42.0/24")
        )
    )
)

iot: Network = Network(
    name="iot-network",
    driver=Driver(name="bridge"),
    ipam=Ipam(
        driver=Driver(),
        config=IpamConfig(
            network=IPv4Network("172.24.0.0/24")
        )
    )
)

adguard = DNS(ip=IPv4Address("192.168.1.15"))
cloudflare = DNS(ip=IPv4Address("1.1.1.1"))

deconz: Service = Service(
    name="deconz",
    restart="unless-stopped",
    image=Image(
        name="marthoc/deconz",
        version="latest"
    ),
    environments=Environments(
        Environment("DEBAIN_FRONTEND", "noninteractive"),
        Environment("DECONZ_DEVICE", "/dev/ttyACM0"),
        Environment("DECONZ_VNC_MODE", 0),
        Environment("DECONZ_VNC_PASSWORD", "1234"),
        Environment("DECONZ_VNC_PORT", 5900),
        Environment("DECONZ_WEB_PORT", 80),
        Environment("DECONZ_WS_PORT", 443),
    ),
    devices=Devices(Device(path=Path("/dev/ttyACM0"))),
    volumes=Volumes(
        Volume(
            name="deconz",
            driver=VDriver(name="local"),
            host=Path("/home/pi/volumes/deconz"),
            container=Path("/root/.local/share/dresden-elektronik/deCONZ"),
            driver_options=VDriverOptions(
                VDriverOption("size", "5GiB"),
                VDriverOption("type", "none"),
                VDriverOption("o", "bild")
            )
        )
    ),
    networks=Networks(
        ContainerNetwork(bshome, ip=IPv4Address("192.168.42.5")),
        ContainerNetwork(iot, ip=IPv4Address("172.24.0.5"))
    ),
    dns=DNSs(adguard, cloudflare)
)

comp = Compose(
    Services(deconz),
    version=2
)

with open("docker-compose/docker-compose.yaml", "w") as docker_file:
    docker_file.write(yaml.safe_dump(comp.asdict()))
