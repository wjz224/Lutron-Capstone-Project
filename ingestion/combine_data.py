import pandas as pd
import os

def combine_data():
    """
    Combines .csv files in the directory "stripped_data" into a single file called "combinedData" store in the directory "combined_data"
    Each .csv file from the directory "stripped_data" will have an added column named "city" that is filled with the name of their respective city

    Function must be be ran while in the "ingestion" directory to find the "stripped_data" and "combined_data directories".
    no parameters
    """
    # list constants that hold the identified similar names
    column_map = {
        "issued_date" : {"issue_date", "job_start_date", "issued_date", "permitissuedate"},
        "contractor" : {"contractor_company_name", "contact_1_name","firm_name", "contractor_name", "contractorname"},
        "latitude" : {"latitude","gis_latitude", "lat"},
        "longitude" : {"longitude","gis_longitude", "lng"}
    }


    # dataframe to store the combined data of all the cities after standardization
    combined_df = pd.DataFrame()

    # pointing towards the directory with our stripped data
    os.chdir("./stripped_data")

    # for loop that will append the data to the lists
    for file in os.listdir(os.getcwd()):
        # dataframe to store the standardized data for each city
        standardized_df = pd.DataFrame()
        # get file name using os.path.basename(file) and the file extension
        city_name, file_extension = os.path.splitext(file)
        # read all files that end with .csv
        if file_extension == ".csv":
            city = pd.read_csv(file)
            # go through column dictionary. dst_column is the standardized column name and src_column are the potential columns names from the data sets
            for dst_column, src_columns in column_map.items():
                # go through each src_column name and check if the src_column name is in the city"s columns.
                for src_column in src_columns:
                    # if the src_column is found, than copy over the city"s src_column to the standardized_df dataframe"s dst_column
                    if src_column in city.columns:
                        # copy over the city"s src_column to the standardized_df dataframe"s dst_column
                        standardized_df[dst_column] = pd.Series(city[src_column])
            # set the dataframe for the current city"s "city" column to the city_name which is the file"s name.
            standardized_df["city"] = city_name
            # concat the city data frame and the current combined data frame
            combined_df = pd.concat([combined_df, standardized_df])

    # create csv with the dataframe with the combined data and store it in the combined_data folder
    combined_df.to_csv("../combined_data/combinedData.csv")
    # change back to previous directory so it doesnt change directory after this wrapper function finishes
    os.chdir("..")

if __name__ == "__main__":
    combine_data()
