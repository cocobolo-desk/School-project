import unittest
import maps_and_cycling
import geo_classes


class TestMaps_And_Cycling(unittest.TestCase):

    def setUp(self):
        self.filename1 = 'e18_500m.json'
        self.data_dict1 = maps_and_cycling.read_json(self.filename1)
        self.list_instances1 = maps_and_cycling.create_instances(self.data_dict1)

        self.filename2 = 'gamla_stan.json'
        self.data_dict2 = maps_and_cycling.read_json(self.filename2)
        self.list_instances2 = maps_and_cycling.create_instances(self.data_dict2)

    def test_check_friendliness(self):

        feature = {"type": "Feature",
                   "geometry": {"type": "LineString",
                                "coordinates": [[18.226315, 59.5489354],
                                                [18.224599, 59.5475604]]},
                   "properties": {"highway": "cycleway",
                                  "int_ref": "E 18",
                                  "lanes": "2"}}
        self.assertEqual(maps_and_cycling.check_friendliness(feature), True)
        feature['properties']['highway'] = 'road'
        self.assertEqual(maps_and_cycling.check_friendliness(feature), False)
        feature['properties']['cycleway'] = 'no'
        self.assertEqual(maps_and_cycling.check_friendliness(feature), False)
        feature['properties']['cycleway'] = 'yes'
        self.assertEqual(maps_and_cycling.check_friendliness(feature), True)
        feature['properties']['cycleway'] = 'no'
        feature['properties']['bicycle'] = 'something'
        self.assertEqual(maps_and_cycling.check_friendliness(feature), True)

    def test_sum_path_lengths(self):
        total_length1, bicycle_length1 = maps_and_cycling.sum_path_lengths(self.list_instances1)
        self.assertEqual(round(total_length1, 2), 0.9)
        self.assertEqual(round(bicycle_length1, 2), 0)

        total_length2, bicycle_length2 = maps_and_cycling.sum_path_lengths(self.list_instances2)
        self.assertEqual(round(total_length2, 2), 27.16)
        self.assertEqual(round(bicycle_length2, 2), 11.32)

    def test_get_pdf_name(self):
        filename = 'abc.a.json'
        with self.assertRaises(NameError):
            maps_and_cycling.get_pdf_name(filename)

