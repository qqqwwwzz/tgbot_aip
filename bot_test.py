import unittest
from bot import calculation

class bot_test(unittest.TestCase):
    def test(self):
        self.assertEqual(calculation(90),2900)
    def test1(self):
        self.assertEqual(calculation(89),2880)
if __name__ == "__main__":
    unittest.main()