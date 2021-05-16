import unittest
import sys; sys.path.append('../lib') 

from welford import WelfordAverage

class TestWelford(unittest.TestCase):
    def test_basic(self):
        w = WelfordAverage()
        data = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21]

        for x in data:
            w.update(x)

        count, avg, _ = w.averages()

        self.assertEqual(count, len(data))
        self.assertEqual(avg, 11)
    
if __name__ == '__main__':
    unittest.main()
