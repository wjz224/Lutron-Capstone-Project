import pandas as pd # pip install pandas
import os

def combine_data():
    # list constants that hold the identified similar names
    column_map = {
        "issued_date" : {'issue_date', 'job_start_date', 'issued_date', 'permitissuedate'},
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
        # read all files that end with .csv
        if file.endswith('.csv'):
            city = pd.read_csv(file)
            # go through column dictionary. dst_column is the standardized column name and src_column are the potential columns names from the data sets
            for dst_column, src_columns in column_map.items():
                # go through each src_column name and check if the src_column name is in the city's columns.
                for src_column in src_columns:
                    # if the src_column is found, than copy over the city's src_column to the standardized_df dataframe's dst_column
                    if(src_column in city.columns):
                        # copy over the city's src_column to the standardized_df dataframe's dst_column
                        standardized_df[dst_column] = pd.Series(city[src_column])
            # get file name using os.path.basename(file)
            city_name, file_extension = os.path.splitext(file)
            # set the dataframe for the current city's "city" column to the city_name which is the file's name.
            standardized_df['city'] = city_name
            # list to hold the city and the combined data frame for concat
            combine = [combined_df, standardized_df]
            # concat the city data frame and the current combined data frame
            combined_df = pd.concat(combine)
            
    # create csv with the dataframe with the combined data and store it in the combined_data folder
    combined_df.to_csv('../combined_data/combinedData.csv')\

# main method combine_data()
def main():
    combine_data()
    
# call main
if __name__ == "__main__":
    main()       
