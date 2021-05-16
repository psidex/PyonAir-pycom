import unittest
import sys; sys.path.append('../lib') 

import strings as s

class TestStrings(unittest.TestCase):
    def test_all(self):
        # Make sure all of our constants haven't changed somehow
        self.assertEqual(type(s.csv_timestamp_template), str)
        self.assertEqual(type(s.headers_dict_v4), dict)
        self.assertEqual(type(s.status_header), list)
        self.assertEqual(type(s.config_filename), str)
        self.assertEqual(type(s.TPP), dict)
        self.assertEqual(type(s.TP), dict)
        self.assertEqual(type(s.PP), dict)
        self.assertEqual(type(s.T), dict)
        self.assertEqual(type(s.P), dict)
        self.assertEqual(type(s.G), dict)

    
if __name__ == '__main__':
    unittest.main()
