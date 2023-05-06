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

# python3 intersect-wesm-by-state.py 

# Set AWS credentials
def main():    
    s3 = get_creds()
    
    print("Downloading files needed...")
    for fl in [WESM, STATES]:
        download(s3, fl)
       
    print("Loading in Geopandas...")    
    wesm = gp.read_file(WESM).to_crs(26914)
    states = gp.read_file(STATES).to_crs(26914)   
     
    states['geometry'] = states.geometry.buffer(0)
    
    for i, st in states.iterrows():        
        state_gpkg = os.path.join(STATES_DIR, f"{st['NAME']}.gpkg")
        print(f"Making state intersect {state_gpkg}")
        state = states[states['NAME'] == st['NAME']]
        selection = get_intersect(state, wesm)
        
        selection.to_crs(WESM_CRS).to_file(state_gpkg, driver="GPKG")
        
    #     print(f"Uploading... {state_gpkg}")   
    #     s3.upload_file(state_gpkg, WESM_BUCKET, state_gpkg)   
    
def get_intersect(state, wesm):
    state_geom = state.geometry.values[0]
    mask = wesm.intersects(state_geom)
    selection = wesm.loc[mask]
    
    return selection
 
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
    STATES_DIR = os.path.join(DATA, "wesm-by-state")
    WESM = "data/WESM-clean.gpkg"
    STATES = "data/us-states.gpkg"
    WESM_CRS = "4269"
    
    os.makedirs(STATES_DIR, exist_ok=True)
    
    main()