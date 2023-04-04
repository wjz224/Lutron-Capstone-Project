import unittest
import pandas as pd
import os
import csv
from ingestion.combine_data import combine_data
class CombineTest(unittest.TestCase):
    def test_combine(self, test_data):
        # temporary csv file that will contain our test data
        tmp_file = "./tmp.csv"
        # write our test data into the temporary file
        with open(tmp_file, 'w') as file:
            writer = csv.writer(file)
            writer.writerows(test_data)
        # check if the resulting data frame from combine_data matches with our expected output
        pd.testing.assert_frame_equal()
        # clean the temporary file
        os.remove(tmp_file)
        pass
    
if __name__ == "__main__":
    unittest.main()