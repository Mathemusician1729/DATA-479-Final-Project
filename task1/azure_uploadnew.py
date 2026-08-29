# Python script for fast upload of our NOAA GSOD data subset to the Microsoft Azure Blob Storage
# The subset consists of 40 different stations across various locations in the world 
# The subset contains data of all 40 stations across 3 decades in 3-year intervals, from 1999-2001, 2009-2011, and 2019-2021

import requests
import os
import time
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient
from concurrent.futures import ThreadPoolExecutor, as_completed

load_dotenv()
CONTAINER = "raw-data"
CONNECTION_STRING = os.getenv("connection_string")

years = [1999, 2000, 2001, 2009, 2010, 2011, 2019, 2020, 2021]
stations = []

with open("task1/stations.txt") as f:
    for line in f:
        id = line.strip().split('- ')[1]
        stations.append(id)

blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
container = blob_service_client.get_container_client(CONTAINER)

def upload_one(year, station):
    csv = requests.get(f"https://noaa-gsod-pds.s3.amazonaws.com/{year}/{station}.csv")
    filename = f"{year}/{station}.csv"
    container.upload_blob(name=filename, data=csv.content, overwrite=True)
    return filename

jobs = [(year, station) for year in years for station in stations]
results = {}

for workers in [40, 45, 50]:
    start_time = time.perf_counter()
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(upload_one, year, station) for year, station in jobs]
        for future in as_completed(futures):
            filename = future.result()

    end_time = time.perf_counter()
    elapsed = end_time - start_time
    results[workers] = elapsed
    print(f"workers={workers}: {elapsed:.2f} seconds")