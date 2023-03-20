"""This script is used to download data from cities  which use Socrata APIs"""

from sodapy import Socrata
import pandas as pd
import logging

# dictionary of the city api urls and their dataset ids
CITIES: "dict[str, str]" = {"data.cityofnewyork.us":"dm9a-ab7w",
        "data.lacity.org":"nbyu-2ha9",
        "data.austintexas.gov": "3syk-w9eu",
        "data.cityofchicago.org": "ydr8-5enu",
        "data.mesaaz.gov": "2gkz-7z4f"}

def get_data(url, dataset_id) -> None:
    """
    Pulls data from a Socrata API and saves it as a csv file
    :param url: the url of the api
    :param dataset_id: the id of the dataset
    :return: None
    """
    client = Socrata(url, None)
    results = client.get(dataset_id)
    df = pd.DataFrame.from_dict(results)
    # Uses part of the url as the name of the csv file
    df.to_csv(f"raw_data/{url.split('.')[1]}.csv")
    print(f"Saved {url.split('.')[1]}.csv")

def main():
    for city in CITIES:
        # The API sometimes times out, so this loop will try to get the data until it succeeds
        while 1:
            try:
                get_data(city, CITIES[city])
                break
            except Exception as e:
                logging.error(e)
                pass

if __name__ == "__main__":
    main()
