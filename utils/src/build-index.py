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

# python3 utils/build-index.py "CA_SantaClaraCounty_2020"

# Set AWS credentials
def main():    
    s3 = get_creds()
    
    # Download WESM
    if not os.path.exists(WESM):
        s3.download_file(WESM_BUCKET, WESM, WESM, ExtraArgs={'RequestPayer':'requester'})
    
    print("Reading WESM...")
    gp_wesm = gp.read_file(WESM)
    filtered = gp_wesm[gp_wesm.workunit == WORKUNIT]
    # filtered.to_file(f"{DATA_DIR}/filter-testing.gpkg", driver="GPKG")
    
    for index, row in filtered.iterrows():
        workunit = row.workunit
        horiz_crs = row.horiz_crs
        vert_crs = row.vert_crs
        native_crs = "epsg:" + horiz_crs
        lpc_prefix = parse_link(row)
        pages = get_pages(s3, lpc_prefix)
        df = []
        parse_pages(df, s3, pages, horiz_crs, workunit, lpc_prefix, vert_crs)
        
    print("Creating GPKG...")
    gpkgName = lpc_prefix.split("/")[-2]
    gpkg_native = os.path.join(INDEX_DIR, (gpkgName + "_index_" + str(horiz_crs) + ".gpkg"))
    gpkg_wgs = os.path.join(INDEX_DIR, (gpkgName + "_index_" + str(4326) + ".gpkg"))
    gfd = gp.GeoDataFrame(df, crs=native_crs)
    gfd.to_crs(native_crs).to_file(gpkg_native, driver="GPKG")
    gfd.to_crs("EPSG:4326").to_file(gpkg_wgs, driver="GPKG")
    
    print(f"Uploading... {gpkg_native}")   
    s3.upload_file(gpkg_native, WESM_BUCKET, gpkg_native)    
    s3.upload_file(gpkg_wgs, WESM_BUCKET, gpkg_wgs)
    
 
def parse_pages(df, s3, pages, horiz_crs, workunit, lpc_prefix, vert_crs):
    for page in pages:
        for obj in page['Contents']:
            usgs_loc = obj['Key']
            print(usgs_loc)
            laz_json, laz_name = get_laz_meta(s3, usgs_loc)           
            poly = bbox(laz_json)  
            write_df(df, horiz_crs, laz_name, workunit, lpc_prefix, usgs_loc, vert_crs, laz_json, poly)                 
        
def write_df(df, horiz_crs, laz_name, workunit, lpc_prefix, usgs_loc, vert_crs, laz_json, poly):
    df.append(
        {
            'file_name':laz_name,
            'workunit': workunit,
            'project_prefix': lpc_prefix,
            'usgs_loc':usgs_loc,
            'native_horiz_crs':horiz_crs,
            'native_vert_crs':vert_crs,
            'json_data': str(laz_json),
            'geometry': poly
        }
    )


def get_laz_meta(s3, usgs_loc):
    laz_name = os.path.basename(usgs_loc)
    part_laz_file=os.path.join(PART_DIR, laz_name)
    part_laz = s3.get_object(Bucket=USGS_BUCKET, Key=usgs_loc, RequestPayer="requester", Range="bytes=0-10000")
    body = part_laz["Body"].read()
    with open(part_laz_file, "wb") as f:
        f.write(body)            
    
    pdalinfo = """
        pdal info --summary %s
    """ % (part_laz_file)
    laz_meta = sub.check_output(pdalinfo, shell=True)
    laz_json = json.loads(laz_meta) 
    
    return laz_json, laz_name

def bbox(laz_json):    
    minx = laz_json['summary']['bounds']['minx']
    miny = laz_json['summary']['bounds']['miny']
    maxx = laz_json['summary']['bounds']['maxx']
    maxy = laz_json['summary']['bounds']['maxy']
    
    poly = Polygon([[minx, miny],
                    [maxx, miny],
                    [maxx, maxy],
                    [minx, maxy],
                    [minx, miny]])
    
    return poly

def get_pages(s3, lpc_prefix):
    paginator = s3.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=USGS_BUCKET, Prefix=lpc_prefix, RequestPayer="requester", PaginationConfig={'MaxItems': 3}) # PaginationConfig={'MaxItems': 1}
    
    return pages

def parse_link(row):
    print("Restructure lpc_link to point to USGS AWS cache")
    splitLink = re.split('projects|Projects', row.lpc_link)[1]
    if splitLink[-1] == "/":
        lpc_prefix = "Projects" + splitLink
    else:
        lpc_prefix = "Projects" + splitLink + "/"

    return lpc_prefix
    
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
    WORKUNIT = sys.argv[1]
    DATA_DIR = "data"
    INDEX_DIR = os.path.join(DATA_DIR, "index-indv")
    PART_DIR = os.path.join(DATA_DIR, "partial-files")
    WESM = "data/WESM.gpkg"
    
    os.makedirs(INDEX_DIR, exist_ok=True)
    os.makedirs(PART_DIR, exist_ok=True)
    
    main()
    