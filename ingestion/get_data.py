import logging
import pandas as pd
from sodapy import Socrata

# Dictionary of cities and their corresponding API information
META_CITY = {"new_york":("socrata", "data.cityofnewyork.us", "dm9a-ab7w"),
            "chicago": ("socrata", "data.cityofchicago.org", "ydr8-5enu"),
            "mesa": ("socrata", "data.mesaaz.gov", "2gkz-7z4f"),
            "la": ("socrata", "data.lacity.org", "nbyu-2ha9"),
            "austin": ("socrata", "data.austintexas.gov", "3syk-w9eu"),
            "philly": ("non_socrata", "https://phl.carto.com/api/v2/sql?filename=permits&format=csv&skipfields=cartodb_id,the_geom,the_geom_webmercator&q=SELECT%20*,%20ST_Y(the_geom)%20AS%20lat,%20ST_X(the_geom)%20AS%20lng%20FROM%20permits%20WHERE%20permitissuedate%20%3E=%20%272016-01-01%27")}

def get_data(url, location):
    """
    Pulls data from a Non-Socrata source and saves it as a csv file
    :param url: the url of the api
    :return: None
    """
    # Use Pandas to read the CSV file from the URL
    df = pd.read_csv(url)
    # Save the CSV file to the current directory
    df.to_csv(f"ingestion/raw_data/{location}.csv", index=False)
    logging.info(f"Saved {location}.csv")

def get_socrata_data(url, dataset_id, location):
    """
    Pulls data from a Socrata API and saves it as a csv file
    :param url: the url of the api
    :param dataset_id: the id of the dataset
    """
    client = Socrata(url, None)
    results = client.get(dataset_id)
    df = pd.DataFrame.from_dict(results)
    # Uses part of the url as the name of the csv file
    df.to_csv(f"ingestion/raw_data/{location}.csv")
    logging.info(f"Saved {location}.csv")

def main():
    locations = ["philly"]
    for place in locations:
        meta = META_CITY[place]
        if meta[0] == "socrata":
            fail_count = 0
            while 1:
                try:
                    get_socrata_data(meta[1], meta[2], place)
                    break
                except Exception as e:
                    logging.error(e)
                    fail_count += 1
                    if fail_count == 3:
                        logging.error(f"Failed to get data from {place}")
                        break
                    pass
        elif meta[0] == "non_socrata":
            try:
                get_data(meta[1], place)
            except Exception as e:
                logging.error(e)


if __name__ == "__main__":
    main()
