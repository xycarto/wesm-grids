import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gp

import boto3
import sys
import re
import subprocess as sub
import json
from shapely.geometry import Polygon
import pyproj

# python3 clean-wesm.py 

# Set AWS credentials
def main():    
    s3 = get_creds()
    
    print("Downloading files needed...")
    for fl in [WESM]:
        download(s3, fl)
       
    print("Loading in Geopandas...")    
    wesm = gp.read_file(WESM).explode(index_parts=True)
    wesm_proj = wesm.to_crs(26914)
    wesm_crs = wesm.crs
    
    print("Cleaning WESM...")
    df = []
    for ind, row in wesm_proj.iterrows():
        row['geometry'] = row['geometry'].exterior
        row['geometry'] = Polygon(row['geometry'].coords)
        
        print("making area...")
        row['area'] = row['geometry'].area  
        
        if row['area'] > 5000:
            print(row['workunit'])
            row['geometry'] = row.geometry.buffer(0)
            df.append(row)
            
    gfd = gp.GeoDataFrame(df, crs="epsg:26914").dissolve(by='workunit')
    gfd.to_file("data/test-clean.gpkg", driver="GPKG")
    gfd.to_crs(wesm_crs).to_file("data/WESM-clean.gpkg", driver="GPKG")
            

def download(s3, fl):
    if not os.path.exists(fl):      
        s3.download_file(WESM_BUCKET, fl, fl, ExtraArgs={'RequestPayer':'requester'})
    
def get_creds():
    s3 = boto3.client(
        's3',
        aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name = 'us-west-2',
    )

    return s3

if __name__ == "__main__":
    
    WESM_BUCKET="wesm"
    DATA= "data"
    WESM = "data/WESM.gpkg"
    
    os.makedirs(DATA, exist_ok=True)
    
    main()