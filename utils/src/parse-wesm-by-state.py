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

# python3 parse-wesm-by-state.py 

# Set AWS credentials
def main():    
    s3 = get_creds()
    
    # Download WESM gpkg
    if not os.path.exists(WESM):
        s3.download_file(WESM_BUCKET, WESM, WESM, ExtraArgs={'RequestPayer':'requester'})
        
    # Download States gpkg
    if not os.path.exists(WESM):
        s3.download_file(WESM_BUCKET, STATES, STATES, ExtraArgs={'RequestPayer':'requester'})
        
    wesm = gp.read_file(WESM)
    states = gp.read_file(STATES)
    
    for i, st in states.iterrows():
        state = states[states['NAME'] == st['NAME']]
        state_gpkg = os.path.join(STATES_DIR, f"{st['NAME']}.gpkg")
        selection = get_intersect(state, wesm)
        
        selection.to_file(state_gpkg, driver="GPKG")
        
        print(f"Uploading... {state_gpkg}")   
        s3.upload_file(state_gpkg, WESM_BUCKET, state_gpkg)   
    
def get_intersect(state, wesm):
    state_geom = state.geometry.values[0]
    mask = wesm.intersects(state_geom)
    selection = wesm.loc[mask]
    
    return selection 
    
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
    DATA_DIR = "data"
    STATES_DIR = os.path.join(DATA_DIR, "wesm-by-state")
    WESM = "data/WESM.gpkg"
    STATES = "data/us-states.gpkg"
    
    os.makedirs(STATES_DIR, exist_ok=True)
    
    main()