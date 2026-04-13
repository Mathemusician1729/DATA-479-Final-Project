# Python script for fast upload of the NOAA GSOD data subset
# The subset consists of 40 different stations across various locations in the world 
# The subset contains data of all 40 stations across 3 3-year intervals, from 1999-2001, 2009-2011, and 2019-2021

import requests
import os
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

load_dotenv() # load all variables from .env, which includes the connection string to the container in azure blob storage
CONTAINER = "raw-data" # name of the container in the azure blob storage
CONNECTION_STRING = os.getenv("connection_string") # get azure connection string to the storage account in azure blob storage

# define years for the subset of data being uploaded 
years = [1999, 2000, 2001, 2009, 2010, 2011, 2019, 2020, 2021]
stations = []

# open the 'stations.txt' which contains the country the station is from, and its ID for each of the 40 selected countries
# extract only the station's ID and add it to the station IDs list
with open("C:/Users/trand/DATA-479-Final-Project/task1/stations.txt") as f:
    for line in f:
        id = line.strip().split('- ')[1]
        stations.append(id)

# create connection to the azure blob storage container
blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
container = blob_service_client.get_container_client(CONTAINER)

# for each year, upload the csv for each station (labeled 'stationID.csv') as a blob in the container. 
# each csv will be stored under the folder with its respective year
for year in years:
    for station in stations:
        # get csv file from the link which downloads it from the s3 bucket
        csv = requests.get(f"https://noaa-gsod-pds.s3.amazonaws.com/{year}/{station}.csv") 

        # set filename to the form 'year/stationID.csv'
        # Creates a folder for that year if not yet created, and stores the csv under that folder
        filename = f"{year}/{station}.csv"

        # upload csv as blob to azure storage
        container.upload_blob(name=filename, data=csv.content, overwrite=True) 
        print(f"Uploaded {filename}")