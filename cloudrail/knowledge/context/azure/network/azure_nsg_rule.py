from enum import Enum
from typing import Tuple, List, Optional, Union

from cloudrail.knowledge.context.aws.aws_connection import ConnectionDirectionType
from cloudrail.knowledge.context.azure.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.ip_protocol import IpProtocol


class NetworkSecurityRuleActionType(str, Enum):
    ALLOW = 'Allow'
    DENY = 'Deny'


class PortSet:

    def __init__(self, port_ranges: List[Tuple[int, int]]):
        self.port_ranges: List[Tuple[int, int]] = port_ranges

    def extend(self, port_ranges: List[Union[int, str, Tuple[int, int]]]):
        self.port_ranges.extend(port_ranges)

    def add(self, port_range: Union[int, str, Tuple[int, int]]):
        type_exception = TypeError('port_range argument must be either an Integer, a (int, int) tuple, or a string representing a number, '
                                   'or a string representing a range of numbers (like 1-10)')
        if isinstance(port_range, int):
            self.port_ranges.append((port_range, port_range))
        elif isinstance(port_range, str):
            ports = port_range.replace(' ', '').split('-')
            if len(ports) == 1:
                port = int(ports[0])
                self.port_ranges.append((port, port))
            elif len(ports) == 2:
                self.port_ranges.append((int(ports[0]), int(ports[1])))
            else:
                raise type_exception
        elif isinstance(port_range, tuple) and len(port_range) == 2:
            self.port_ranges.append(port_range)
        else:
            raise type_exception

    def __add__(self, other):
        """
        other: Union[PortSet, Tuple[int, int], int, List[Tuple[int, int]]]
        """
        return PortSet(self.port_ranges + self._to_port_set(other).port_ranges)

    def __sub__(self, other):
        """
        other: Union[PortSet, Tuple[int, int], int, List[Tuple[int, int]]]
        """
        port_ranges = []
        for self_port_range in self.port_ranges:
            for other_port_range in other.port_ranges:
                low1, high1 = self_port_range
                low2, high2 = other_port_range

                if low2 < low1:
                    low2 = low1

                if low1 == low2:
                    if high1 <= high2:
                        continue
                    port_ranges.append((high2 + 1, high1))
                elif low1 < low2:
                    port_ranges.append((low1, low2 - 1))
                    if high2 < high1:
                        port_ranges.append((high2 + 1, high1))

        return PortSet(port_ranges)

    @staticmethod
    def _to_port_set(other):
        # other: List[Tuple[int, int]]
        if isinstance(other, list):
            return PortSet(other)

        # other: PortSet
        if isinstance(other, PortSet):
            return other

        # other: int
        if isinstance(other, int):
            return PortSet([(other, other)])

        # other: Tuple[int, init]
        return PortSet([other])

    @staticmethod
    def create_all_ports_set():
        return PortSet([(0, 65535)])

    # get_range_numbers_overlap
    def intersection(self, other):
        other_port_set = self._to_port_set(other)
        port_ranges = []
        for self_port_range in self.port_ranges:
            for other_port_range in other_port_set.port_ranges:
                low1, high1 = self_port_range
                low2, high2 = other_port_range
                if low2 <= low1 <= high2 or low1 <= low2 <= high1:
                    low: int = low1 if low1 > low2 else low2
                    high: int = high2 if high1 > high2 else high1
                    port_ranges.append((low, high))

        return PortSet(port_ranges)

    def __bool__(self):
        return bool(self.port_ranges)

    def __repr__(self):
        return ', '.join([f'{low}-{high}' for low, high in self.port_ranges])

    def __contains__(self, item: int):
        """
        Magic method that checks if a specific port is contained in this PortSet
        Currently only supporting integers
        """
        if isinstance(item, int):
            return any(low <= item <= high for low, high in self.port_ranges)

    # def get_range_numbers_dis_overlap(range1: Tuple[int, int], range2: Tuple[int, int]) -> List[Tuple[int, int]]:
    #     low1, high1 = range1
    #     low2, high2 = range2
    #     overlap_range = get_range_numbers_overlap(range1, range2)
    #
    #     if overlap_range != EMPTY_RANGE:
    #         overlap_low, overlap_high = overlap_range
    #         dis_overlap_list: List[Tuple[int, int]] = []
    #         if overlap_low > low1:
    #             dis_overlap_list.append((low1, overlap_low - 1))
    #         elif overlap_low > low2:
    #             dis_overlap_list.append((low2, overlap_low - 1))
    #
    #         if overlap_high < high1:
    #             dis_overlap_list.append((overlap_high + 1, high1))
    #         elif overlap_high < high2:
    #             dis_overlap_list.append((overlap_high + 1, high2))
    #
    #         return dis_overlap_list
    #     else:
    #         return [range1, range2]


class AzureNetworkSecurityRule(AzureResource):
    """
        Attributes:
            name: The NSG name
            priority
            direction
            access
            protocol
            source_port_ranges
            destination_port_ranges
            source_address_prefixes
            destination_address_prefixes
            network_security_group_name
    """

    def get_keys(self) -> List[str]:
        return [self.network_security_group_name, self.priority]

    def get_cloud_resource_url(self) -> Optional[str]:
        pass  # TOOD

    @property
    def is_tagable(self) -> bool:
        return False

    def __init__(self,
                 name: str,
                 priority: int,
                 direction: ConnectionDirectionType,
                 access: NetworkSecurityRuleActionType,
                 protocol: IpProtocol,
                 destination_port_ranges: PortSet,
                 source_address_prefixes: List[str],
                 destination_address_prefixes: List[str],
                 network_security_group_name: str
                 ):
        super().__init__(AzureResourceType.AZURERM_NETWORK_SECURITY_GROUP)
        self.name: str = name
        self.priority: int = priority
        self.direction: ConnectionDirectionType = direction
        self.access: NetworkSecurityRuleActionType = access
        self.protocol: IpProtocol = protocol
        self.destination_port_ranges: PortSet = destination_port_ranges
        # read the docs as this can contain an enum as well, (Optional) CIDR or source IP range or * to match any IP. Tags such as ‘VirtualNetwork’, ‘AzureLoadBalancer’ and ‘Internet’ can also be used
        self.source_address_prefixes: List[str] = source_address_prefixes
        # same shit as source
        self.destination_address_prefixes: List[str] = destination_address_prefixes
        self.network_security_group_name: str = network_security_group_name
