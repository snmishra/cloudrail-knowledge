import unittest
from cloudrail.knowledge.context.ip_protocol import IpProtocol


class TestIpProtocol(unittest.TestCase):
    def setUp(self):
        self.function = IpProtocol

    def test_protocol_name_pass(self):
        # Arrange
        ip_proto = 'TCP'
        # Act
        result = self.function(ip_proto)
        # Assert
        self.assertTrue(result.__eq__('TCP'))

    def test_protocol_name_lower_pass(self):
        # Arrange
        ip_proto = 'tcp'
        # Act
        result = self.function(ip_proto)
        # Assert
        self.assertTrue(result.__eq__('TCP'))

    def test_protocol_number_convert_tcp_pass(self):
        # Arrange
        ip_proto = '6'
        # Act
        result = self.function(ip_proto)
        # Assert
        self.assertTrue(result.__eq__('TCP'))

    def test_protocol_number_convert_udp_pass(self):
        # Arrange
        ip_proto = '17'
        # Act
        result = self.function(ip_proto)
        # Assert
        self.assertTrue(result.__eq__('UDP'))

    def test_protocol_number_convert_udp_as_int_pass(self):
        # Arrange
        ip_proto = 17
        # Act
        result = self.function(ip_proto)
        # Assert
        self.assertTrue(result.__eq__('UDP'))

    def test_all_protocols_gcp_none_pass(self):
        # Arrange
        ip_proto = None
        # Act
        result = self.function(ip_proto)
        # Assert
        self.assertTrue(result.__eq__('ALL'))

    def test_all_protocols_aws_pass(self):
        # Arrange
        ip_proto = -1
        # Act
        result = self.function(ip_proto)
        # Assert
        self.assertTrue(result.__eq__('ALL'))

    def test_all_protocols_aws_string_pass(self):
        # Arrange
        ip_proto = '-1'
        # Act
        result = self.function(ip_proto)
        # Assert
        self.assertTrue(result.__eq__('ALL'))

    def test_all_protocols_azure_pass(self):
        # Arrange
        ip_proto = 'Any'
        # Act
        result = self.function(ip_proto)
        # Assert
        self.assertTrue(result.__eq__('ALL'))

    def test_all_protocols_azure_with_repr_pass(self):
        # Arrange
        ip_proto = 'Any'
        # Act
        result = self.function(ip_proto)
        # Assert
        self.assertEqual(result.__repr__(), IpProtocol('ALL'))

    def test_special_ip_proto_pass(self):
        # Arrange
        ip_proto = '14'
        # Act
        result = self.function(ip_proto)
        # Assert
        self.assertTrue(result.__eq__('EMCON'))

    def test_unknown_ip_proto_raise_exception(self):
        # Arrange
        ip_proto = 'Some_strange_unknown_ip_proto'
        # Act and Assert:
        self.assertRaises(ValueError, lambda: self.function(ip_proto))

    def test_contain_tcp_pass(self):
        # Arrange
        ip_proto = 'tcp'
        # Act
        result = self.function(ip_proto)
        # Assert
        self.assertTrue(result.__contains__('TCP'))

    def test_all_contain_tcp_pass(self):
        # Arrange
        ip_proto = 'ALL'
        # Act
        result = self.function(ip_proto)
        # Assert
        self.assertTrue(result.__contains__('TCP'))

    def test_testing_false_17_not_tcp_fail(self):
        # Arrange
        ip_proto = 17
        # Act
        result = self.function(ip_proto)
        # Assert
        self.assertFalse(result.__eq__('TCP'))
