import unittest

from cloudrail.knowledge.utils.port_set import PortSet


class TestPortSet(unittest.TestCase):

    def test_add_ok(self):
        # Arrange
        ports = PortSet([])
        # Act
        ports.add(1)
        ports.add('10')
        ports.add('100-200')
        ports.add('300 -400')
        ports.add('500- 600')
        ports.add('700 - 800')
        ports.add((1000, 2000))
        # Assert
        for port_tuple in ((1, 1), (10, 10), (100, 200), (300, 400), (500, 600), (700, 800), (1000, 2000)):
            self.assertIn(port_tuple, ports.port_ranges)

    def test_add_invalid_values(self):
        # Arrange
        ports = PortSet([])
        # Act/Assert
        for port_tuple in ((-1, 10), (1, 65536), (-2, -1), (65536, 65537), [(1, 2)]):
            with self.assertRaises(TypeError):
                ports.add(port_tuple)

    def test_extend_ok(self):
        # Arrange
        ports = PortSet([])
        # Act
        ports.extend([1, '10', '100-200', '300 -400', '500- 600', '700 - 800', (1000, 2000)])
        # Assert
        for port_tuple in ((1, 1), (10, 10), (100, 200), (300, 400), (500, 600), (700, 800), (1000, 2000)):
            self.assertIn(port_tuple, ports.port_ranges)

    def test_extend_invalid_values(self):
        # Arrange
        ports = PortSet([])
        # Act/Assert
        for port_tuple in ((-1, 10), (1, 65536), (-2, -1), (65536, 65537), [(1, 2)]):
            with self.assertRaises(TypeError):
                ports.extend([port_tuple])

    def test____add__ok(self):
        # Arrange
        ports = PortSet([])
        # Act
        ports = ports + 1
        ports = ports + '10'
        ports = ports + '100-200'
        ports = ports + '300 -400'
        ports = ports + '500- 600'
        ports = ports + '700 - 800'
        ports = ports + (1000, 2000)
        # Assert
        for port_tuple in ((1, 1), (10, 10), (100, 200), (300, 400), (500, 600), (700, 800), (1000, 2000)):
            self.assertIn(port_tuple, ports.port_ranges)

    def test___sub__1(self):
        # Arrange
        ports = PortSet(['100-200', '250-300'])
        # Act
        ports = ports - '180-260'
        # Assert
        self.assertEqual(len(ports.port_ranges), 2)
        self.assertIn((100, 179), ports.port_ranges)
        self.assertIn((261, 300), ports.port_ranges)

    def test___sub__2(self):
        # Arrange
        ports = PortSet(['100-200', '250-300'])
        # Act
        ports = ports - '1000-2000'
        # Assert
        self.assertEqual(len(ports.port_ranges), 2)
        self.assertIn((100, 200), ports.port_ranges)
        self.assertIn((250, 300), ports.port_ranges)

    def test___sub__3(self):
        # Arrange
        ports = PortSet(['100-200', '250-300'])
        # Act
        ports = ports - '10-20'
        # Assert
        self.assertEqual(len(ports.port_ranges), 2)
        self.assertIn((100, 200), ports.port_ranges)
        self.assertIn((250, 300), ports.port_ranges)

    def test___sub__4(self):
        # Arrange
        ports = PortSet(['100-200', '250-300'])
        # Act
        ports = ports - '210-220'
        # Assert
        self.assertEqual(len(ports.port_ranges), 2)
        self.assertIn((100, 200), ports.port_ranges)
        self.assertIn((250, 300), ports.port_ranges)

    def test___sub__5(self):
        # Arrange
        ports = PortSet(['100-200', '250-300'])
        # Act
        ports = ports - '180-190'
        # Assert
        self.assertEqual(len(ports.port_ranges), 3)
        self.assertIn((100, 179), ports.port_ranges)
        self.assertIn((191, 200), ports.port_ranges)
        self.assertIn((250, 300), ports.port_ranges)

    def test___sub__6(self):
        # Arrange
        ports = PortSet(['100-200', '250-300'])
        # Act
        ports = ports - '250-260'
        # Assert
        self.assertEqual(len(ports.port_ranges), 2)
        self.assertIn((100, 200), ports.port_ranges)
        self.assertIn((261, 300), ports.port_ranges)

    def test___sub__7(self):
        # Arrange
        ports = PortSet(['100-200', '250-300'])
        # Act
        ports = ports - '251-260'
        # Assert
        self.assertEqual(len(ports.port_ranges), 3)
        self.assertIn((100, 200), ports.port_ranges)
        self.assertIn((250, 250), ports.port_ranges)
        self.assertIn((261, 300), ports.port_ranges)

    def test_create_all_ports_set(self):
        # Arrange / Act
        ports = PortSet.create_all_ports_set()
        # Assert
        self.assertEqual(len(ports.port_ranges), 1)
        self.assertIn((0, 65535), ports.port_ranges)

    def test___contains__in(self):
        # Arrange
        ports = PortSet(['100-150'])
        # Act / Assert
        self.assertTrue(100 in ports)
        self.assertTrue(150 in ports)
        self.assertTrue(110 in ports)

    def test___contains__not_in(self):
        # Arrange
        ports = PortSet(['100-150'])
        # Act / Assert
        self.assertFalse(0 in ports)
        self.assertFalse(-1 in ports)
        self.assertFalse(50 in ports)
        self.assertFalse(151 in ports)
        self.assertFalse(1000000 in ports)

    def test_intersection_1(self):
        # Arrange
        ports = PortSet(['100-150'])
        # Act
        intersected = ports.intersection('101')
        # Assert
        self.assertIn(101, intersected)

    def test_intersection_2(self):
        # Arrange
        ports = PortSet(['100-150'])
        # Act
        intersected = ports.intersection('101-103')
        # Assert
        self.assertEqual(intersected.port_ranges, [(101, 103)])

    def test_intersection_3(self):
        # Arrange
        ports = PortSet(['100-150'])
        # Act
        intersected = ports.intersection('0-103')
        # Assert
        self.assertEqual(intersected.port_ranges, [(100, 103)])

    def test_intersection_4(self):
        # Arrange
        ports = PortSet(['100-150'])
        # Act
        intersected = ports.intersection('130-160')
        # Assert
        self.assertEqual(intersected.port_ranges, [(130, 150)])

    def test_intersection_5(self):
        # Arrange
        ports = PortSet(['100-150'])
        # Act
        intersected = ports.intersection([(110, 120), (130, 140)])
        # Assert
        self.assertEqual(intersected.port_ranges, [(110, 120), (130, 140)])

    def test_intersection_6(self):
        # Arrange
        ports = PortSet(['100-150'])
        # Act
        intersected = ports.intersection([(110, 120), (200, 300)])
        # Assert
        self.assertEqual(intersected.port_ranges, [(110, 120)])

    def test_intersection_7(self):
        # Arrange
        ports = PortSet(['100-150'])
        # Act
        intersected = ports.intersection([(0, 200)])
        # Assert
        self.assertEqual(intersected.port_ranges, [(100, 150)])
