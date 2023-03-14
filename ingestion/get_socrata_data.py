from sodapy import Socrata
import pandas as pd

cities: "dict[str, str]" = {"data.cityofnewyork.us":"dm9a-ab7w",
        "data.lacity.org":"nbyu-2ha9",
        "data.austintexas.gov": "3syk-w9eu",
        "data.cityofchicago.org": "ydr8-5enu",
        "data.mesaaz.gov": "2gkz-7z4f"}

def get_data(url, dataset_id):
    client = Socrata(url, None)
    results = client.get(dataset_id)
    df = pd.DataFrame.from_dict(results)
    df.to_csv(f"raw_data/{url.split('.')[1]}.csv")
    print(f"Saved {url.split('.')[1]}.csv")

def main():
    for city in cities:
        while 1:
            try:
                get_data(city, cities[city])
                break
            except:
                pass

if __name__ == "__main__":
    main()
