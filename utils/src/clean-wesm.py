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
    wesm = gp.read_file(WESM).explode(index_parts=True).to_crs(26914)
    wesm_crs = wesm.crs
    
    print("Cleaning WESM...")
    # wesm_proj = wesm.to_crs(26914)
    # wesm_proj['geometry'] = wesm_proj['geometry'].exterior
    # wesm_proj['area'] = wesm_proj['geometry'].area
    
    # wesm['geometry'] = wesm.geometry.buffer(0)
    # wesm_clean = [row['geometry'] = row.geometry.buffer(0) for i, row in wesm.iterrows()]
    df = []
    for ind, row in wesm.iterrows():
        # new_row = row[row['geometry'] == row.geometry.buffer(0)]
        # print(new_row)

        # print(row.geometry)
        # row['geometry'] = row.geometry.buffer(0)
        # row_reproj = row.to_crs(26914)
        # print("getting exterior...")
        row['geometry'] = row['geometry'].exterior
        row['geometry'] = Polygon(row['geometry'].coords)
        # geom = close_geometry(row['geometry'])
        # print(type(geom))
        
        print("making area...")
        row['area'] = row['geometry'].area  
        
        if row['area'] > 5000:
            print(row['workunit'])
            row['geometry'] = row.geometry.buffer(0)
            df.append(row)
            
    gfd = gp.GeoDataFrame(df, crs="epsg:26914").dissolve(by='workunit')
    gfd.to_file("data/test-clean.gpkg", driver="GPKG")
            
        
            
# def close_geometry(geometry):
#     # if geometry.empty or geometry[0].empty:
#     #    return geometry # empty

#     # if(geometry[-1][-1] == geometry[0][0]):
#     #     return geometry  # already closed

#     result = None
#     for linestring in geometry:
#         if result is None:
#           resultstring = linestring.clone()
#         else:
#           resultstring.extend(linestring.coords)

#     geom = Polygon(resultstring)

#     return geom        
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
    WESM = "data/WESM.gpkg"
    
    os.makedirs(DATA, exist_ok=True)
    
    main()