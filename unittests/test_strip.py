import pandas
import unittest
import sys
sys.path.insert(1, "../ingestion")
from strip_data import strip_dataframes

class GetDataTest(unittest.TestCase):
    def test_austin(self):
        data = strip_dataframes(["austin"])
        self.assertIsInstance(data, list)
        self.assertIsInstance(data[0], pandas.DataFrame)

if __name__ == "__main__":
    unittest.main()
