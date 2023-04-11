"""This script pulls data from ether Socrata or directly from a CSV file and saves it as a CSV file."""

import logging
import pandas as pd
from sodapy import Socrata
import os
import sys

# Dictionary of cities and their corresponding API information
META_CITY = {"new_york":("socrata", "data.cityofnewyork.us", "dm9a-ab7w", "job_start_date"),
            "chicago": ("socrata", "data.cityofchicago.org", "ydr8-5enu", "issue_date"),
            "mesa": ("socrata", "data.mesaaz.gov", "2gkz-7z4f", "issued_date"),
            "la": ("socrata", "data.lacity.org", "nbyu-2ha9", "issue_date"),
            "austin": ("socrata", "data.austintexas.gov", "3syk-w9eu", "issue_date"),
            "philly": ("non_socrata", "https://phl.carto.com/api/v2/sql?filename=permits&format=csv&skipfields=cartodb_id,the_geom,the_geom_webmercator&q=SELECT%20*,%20ST_Y(the_geom)%20AS%20lat,%20ST_X(the_geom)%20AS%20lng%20FROM%20permits%20WHERE%20permitissuedate%20%3E=%20%272016-01-01%27"),
            "philly_valuation": ("non_socrata", "https://phl.carto.com/api/v2/sql?q=SELECT * FROM opa_properties_public")}
# Number of times the script will try to get data from a Socrata API
SOCRATA_TRIES = 3
# Max number of rows to call for the Socrata API for testing
ROW_LIMIT = 1_000_000_000

def get_data(url, location) -> None:
    """
    Pulls data from a Non-Socrata source and saves it as a csv file
    :param url: the url of the api
    :param location: the name of the location
    :return: None
    """
    # Use Pandas to read the CSV file from the URL
    df = pd.read_csv(url)
    # Save the CSV file to the current directory
    df.to_csv(f"./raw_data/{location}.csv", index=False)
    logging.info(f"Saved {location}.csv")


def get_socrata_data(url, dataset_id, location, date_column) -> None:
    """
    Pulls data from a Socrata API and saves it as a csv file
    :param url: the url of the api
    :param dataset_id: the id of the dataset
    :param location: the name of the location
    :param date_column: the name of the date column
    """
    client = Socrata(url, None)
    # check if the dataset exists in raw_data
    if f"{location}.csv" in os.listdir("./raw_data"):
        df = pd.read_csv(f"./raw_data/{location}.csv")
        most_recent_date = df[date_column][0]
        results = client.get(dataset_id, where=f"{date_column}>'{most_recent_date}'", order=f"{date_column} DESC", limit=ROW_LIMIT)
        df = pd.DataFrame.from_dict(results).append(df)
    else:
        results = client.get(dataset_id, order=f"{date_column} DESC", limit=ROW_LIMIT)
        df = pd.DataFrame.from_dict(results)
    # Saves dataframe as a csv file
    df.to_csv(f"./raw_data/{location}.csv")
    logging.info(f"Saved {location}.csv")


def main() -> None:
    locations = ["new_york", "chicago", "mesa", "la", "austin", "philly", "philly_valuation"]
    for place in locations:
        meta = META_CITY[place]
        if meta[0] == "socrata":
            fail_count = 0
            while 1:
                try:
                    get_socrata_data(meta[1], meta[2], place, meta[3])
                    break
                except Exception as e:
                    logging.error(e)
                    fail_count += 1
                    if fail_count == SOCRATA_TRIES:
                        logging.error(f"Failed to get data from {place} after {fail_count} tries.")
                        break
                    pass
        elif meta[0] == "non_socrata":
            try:
                get_data(meta[1], place)
            except Exception as e:
                logging.error(e)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout)
    main()
