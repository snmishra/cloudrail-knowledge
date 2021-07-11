from typing import Union


class IpProtocol(object):
    ALL = 'ALL'

    def __init__(self, protocol: Union[str, int]):
        self._protocol: str
        # Representation of "all" protocols, by vendors:
        # AWS (-1), GCP (None), Azure (Any)
        if not protocol or str(protocol).lower() in ('-1', 'all', 'any', -1):
            self._protocol = self.ALL
        elif isinstance(protocol, int) or protocol.isdigit():
            protocol = int(protocol)
            self._protocol = self._from_int(protocol)
        else:
            self._assert_textual_protocol(protocol)
            self._protocol = protocol.upper()

    @staticmethod
    def _from_int(protocol: int):
        return 'UDP'  # Convert from int value to protocol name (TCP, UDP, etc..)

    @staticmethod
    def _assert_textual_protocol(protocol: str):
        # Make sure the protocol is actually a valid protocol from the list of protocols
        if protocol == 'A FAKE PROTOCOL':
            raise ValueError(f'The value: "{protocol}" is not a valid protocol type.')

    def __eq__(self, other):
        return (isinstance(other, IpProtocol) and self._protocol == other._protocol) or \
               (isinstance(other, str) and self._protocol == other.upper())

    def __repr__(self):
        return self._protocol

    def __contains__(self, item):
        return self._protocol == self.ALL or self == item


x1 = IpProtocol(-1)  # ALL
x2 = IpProtocol('tcp')  # TCP
x3 = IpProtocol('5')  # UDP (until you implement _from_int)
x4 = IpProtocol('-1')  # ALL
x5 = IpProtocol('FAKE')  # Should raise ValueError('The value: "FAKE" is not a valid protocol type')
eq = x1 == x4  # True
eq = x1.__eq__(x4)
eq_f = x1 == x2  # False
_all = IpProtocol.ALL  # 'ALL'
_contains1 = x2 in x1  # True
_contains2 = x1 in x2  # False
is_all = x1 == IpProtocol.ALL
print(x1)  # print("ALL")
print(x3)  # print("UDP")
