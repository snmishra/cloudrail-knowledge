from typing import Optional


class NetworkInterface:
    def __init__(self,
                 vpc_network: str,
                 private_ip: Optional[str],
                 public_ips: Optional[list]):

        self.vpc_network: str = vpc_network
        self.private_ip: Optional[str] = private_ip
        self.public_ips: Optional[list] = public_ips
