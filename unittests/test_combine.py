import unittest
import pandas as pd
import os
import csv

class CombineTest(unittest.TestCase):
    def test_combine(self, test_data):
        # Writing test data into a temporary file
        tmp_file = "./tmp.csv"
        with open(tmp_file, 'w') as file:
            writer = csv.writer(file)
            writer.writerows(test_data)
        pass
    
    
if __name__ == "__main__":
    unittest.main();