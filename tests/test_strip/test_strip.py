"""These are the unit tests for the strip_data.py scripts."""

import pandas as pd
import unittest
import os
import logging
import sys
sys.path.insert(1, "../../ingestion")
from strip_data import strip_dataframes

class GetDataTest(unittest.TestCase):
    def test_austin(self, location="austin"):
        """
        Tests the stripping function for Austin and compares the output to the true output. This function is reused for the tests for the other cities
        """
        log = logging.getLogger("test")
        log.debug(f"Testing {location}")
        data = strip_dataframes([location])
        self.assertIsInstance(data, list)
        self.assertIsInstance(data[0], pd.DataFrame)
        true = pd.read_csv(f"./stripped_data_true/{location}_true.csv")
        new = pd.read_csv(f"./stripped_data/{location}.csv")
        self.assertTrue(true.equals(new))
        os.remove(f"./stripped_data/{location}.csv")

    def test_new_york(self):
        """
        Tests the stripping function for New York.
        """
        self.test_austin("new_york")

    def test_chicago(self):
        """
        Tests the stripping function for Chicago.
        """
        self.test_austin("chicago")

    def test_mesa(self):
        """
        Tests the stripping function for Mesa.
        """
        self.test_austin("mesa")

    def test_la(self):
        """
        Tests the stripping function for Los Angeles.
        """
        self.test_austin("la")

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout)
    logging.getLogger("test").setLevel(logging.DEBUG)
    unittest.main()
