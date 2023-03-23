import logging
import pandas as pd

#import ssl
#ssl._create_default_https_context = ssl._create_unverified_context


# Define the URL of the database
# dictionary of the city api urls and their dataset ids
CITIES: "dict[str]" = {'https://phl.carto.com/api/v2/sql?filename=permits&format=csv&skipfields=cartodb_id,the_geom,the_geom_webmercator&q=SELECT%20*,%20ST_Y(the_geom)%20AS%20lat,%20ST_X(the_geom)%20AS%20lng%20FROM%20permits%20WHERE%20permitissuedate%20%3E=%20%272016-01-01%27'}

def get_data(url) -> None:
    """
    Pulls data from a Non-Socrata source and saves it as a csv file
    :param url: the url of the api
    :return: None
    """
    # Use Pandas to read the CSV file from the URL
    df = pd.read_csv(url)
    # Save the CSV file to the current directory
    df.to_csv(f"raw_data/{url.split('.')[0]}.csv", index=False)
    print(f"Saved {url.split('.')[1]}.csv")


def main():
    for city in CITIES:
            try:
                get_data(city)
                break
            except Exception as e:
                logging.error(e)
                pass

if __name__ == "__main__":
    main()

