import unittest
import geo_classes


class TestGeo_Classes(unittest.TestCase):

    def setUp(self):
        """Sets up standard case which is then used in some tests."""
        self.coordinates = [[59.331884596616426, 18.08817041751672],
                            [59.331681433286406, 18.0836374844184],
                            [59.33296288155198, 18.076268740097362]]
        self.name = 'Strandvägen'
        self.bike_friendly = False
        self.myPath = geo_classes.Path(self.coordinates, self.name, self.bike_friendly)

    def testPath(self):
        with self.assertRaises(ValueError):
            # Should not accept anything but bool for bike-friendliness
            geo_classes.Path([[1, 1]], 'hej', 3)
            self.myPath.bicycle_friendly = 'True'

    def test_name(self):
        geo_object = geo_classes.GeoObject('Norrmalmstorg')
        self.assertEqual('Norrmalmstorg', geo_object.name())
        self.assertEqual('Strandvägen', self.myPath.name())

    def test_path_length(self):
        self.assertEqual(self.myPath.path_length(), 1.3326436858479518)

    def test_path___len__(self):
        self.assertEqual(len(self.myPath), 3)

    def test_path__str__(self):
        output = f'\nPath name: Strandvägen' + \
                 f'\nPath length: {int(1000 * 1.3326436858479518)} m' + \
                 f'\nBicycle-friendly: False'
        self.assertEqual(str(self.myPath), output)

    def testPoint(self):
        # Both longitude and latitude should have datatype 'int' or 'float'
        with self.assertRaises(TypeError):
            geo_classes.Point('1', 1)
        with self.assertRaises(TypeError):
            geo_classes.Point(1, '1')

        # Longitude should be between -180 and 180 degrees
        with self.assertRaises(ValueError):
            geo_classes.Point(-181, 1)
        with self.assertRaises(ValueError):
            geo_classes.Point(181, 1)

        # Latitude should be between -90 and 90 degrees
        with self.assertRaises(ValueError):
            geo_classes.Point(1, -91)
        with self.assertRaises(ValueError):
            geo_classes.Point(1, 91)


if __name__ == '__main__':
    unittest.main()
