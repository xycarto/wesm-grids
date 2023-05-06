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
    wesm = gp.read_file(WESM).explode(index_parts=True)
    states = gp.read_file(STATES)
    
    print("Cleaning input files...")
    # wesm['geometry'] = wesm.geometry.buffer(0)
    # wesm_clean = [row['geometry'] = row.geometry.buffer(0) for i, row in wesm.iterrows()]
    for ind, row in wesm.iterrows():
        if row.workunit == "CO_UpperColorado_Hydroflattened_2020" or row.workunit == "FL_WestEvergladesNP_topobathymetric_2018" or AZ_MaricopaPinal_1_2020:
            # new_row = row[row['geometry'] == row.geometry.buffer(0)]
            # print(new_row)

            # print(row.geometry)
            # row['geometry'] = row.geometry.buffer(0)
            pass
        else:
            row['geometry'] = row.geometry.buffer(0)
            print(row)
    # print(wesm_clean)
    # print(type(wesm_clean))
        
    # states['geometry'] = states.geometry.buffer(0)
    
    # for i, st in states.iterrows():        
    #     state_gpkg = os.path.join(STATES_DIR, f"{st['NAME']}.gpkg")
    #     print(f"Making state intersect {state_gpkg}")
    #     state = states[states['NAME'] == st['NAME']]
    #     selection = get_intersect(state, wesm)
        
    #     selection.to_file(state_gpkg, driver="GPKG")
        
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
    WESM = "data/WESM.gpkg"
    STATES = "data/us-states.gpkg"
    
    os.makedirs(STATES_DIR, exist_ok=True)
    
    main()