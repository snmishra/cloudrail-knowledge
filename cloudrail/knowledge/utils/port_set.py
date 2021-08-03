from typing import List, Tuple, Union


class PortSet:

    _MIN_PORT = 0
    _MAX_PORT = 65535

    def __init__(self, port_ranges: List[Tuple[int, int]]):
        self.port_ranges: List[Tuple[int, int]] = port_ranges

    def extend(self, port_ranges: List[Union[int, str, Tuple[int, int]]]):
        self.port_ranges.extend(port_ranges)

    def add(self, port_range: Union[int, str, Tuple[int, int]]):
        type_exception = TypeError(f'port_range argument must be either an Integer, a (int, int) tuple, or a string representing a number, '
                                   f'or a string representing a range of numbers between {self._MIN_PORT} and {self._MAX_PORT} (like 1-10)')
        if isinstance(port_range, int):
            port_tuple = (port_range, port_range)
        elif isinstance(port_range, str):
            ports = port_range.replace(' ', '').split('-')
            if len(ports) == 1:
                port = int(ports[0])
                port_tuple = (port, port)
            elif len(ports) == 2:
                port_tuple = (int(ports[0]), int(ports[1]))
            else:
                raise type_exception
        elif isinstance(port_range, tuple) and len(port_range) == 2:
            port_tuple = port_range
        else:
            raise type_exception

        if port_tuple[0] < self._MIN_PORT or port_tuple[1] > self._MAX_PORT:
            raise type_exception

        self.port_ranges.append(port_tuple)

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
        return PortSet([(PortSet._MIN_PORT, PortSet._MAX_PORT)])

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
