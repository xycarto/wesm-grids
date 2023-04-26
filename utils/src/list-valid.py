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

# python3 list-valid.py California

# Set AWS credentials
def main():    
    s3 = get_creds()
    
    # Download States gpkg
    if not os.path.exists(WESM_STATE):
        s3.download_file(WESM_BUCKET, WESM_STATE, WESM_STATE, ExtraArgs={'RequestPayer':'requester'})
        
    state = gp.read_file(WESM_STATE)
    
    valid = state[
    (state.lpc_category == 'Meets') | 
    (state.lpc_category == 'Meets with variance') |
    (state.lpc_category == 'Expected to meet')
    ]
    
    fin = f"{LIST_DIR}/{STATE}-tmp.txt"
    with open(fin, 'w') as f:
        dfAsString = valid.workunit.to_string(header=False, index=False)
        f.write(dfAsString)
        
    fout = open(f"{LIST_DIR}/{STATE}.txt", "w")
    with open(fin,"r") as tmp:
        for line in tmp:
            new_line = line.strip()
            fout.write(f"{new_line}\n") 
        
    os.remove(fin)
    
def get_creds():
    s3 = boto3.client(
        's3',
        aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name = 'us-west-2',
    )

    return s3
    
    
if __name__ == "__main__":
    
    USGS_BUCKET="usgs-lidar"
    WESM_BUCKET="wesm"
    STATE = sys.argv[1]
    DATA_DIR = "data"
    LIST_DIR = os.path.join("lists", STATE)
    WESM_STATE = os.path.join("data","wesm-by-state", f"{STATE}.gpkg")
    
    os.makedirs(LIST_DIR, exist_ok=True)
    
    main()