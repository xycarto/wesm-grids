# wesm-grids

**IN DEVELOPMENT**

Transform WESM aquisition shapes into index files for available point cloud files available in USGS AWS S3 buckets.  The output is an individual GPKG file indexing the aquisition with attributed information including:

1. Point density
1. Extents of point cloud
1. S3 prefix path
1. Native projection stored as EPSG code

Terrform is being tested as a method to employ multiple EC2s in the process.  The tested method thus far uses an `xargs` approach, where any number of aquisitions (workunits) may be processed. Each acqusition is processed on an individual EC2.

```
cat lists/test-list.txt | xargs -P 2 -t -I % make build workunit=%
```

## TODO

Tested and working. Improvements

1. Linking between scripts
1. Error coding. Not all `workunits` will pass on `make wesm-index`.
1. Less verbose scripts
1. Passing source crs through project
1. The current method is too slow for launching the EC2.  Time is taken up in pulling the needed Docker. Ideally, replaction of the server would suffice.  
1. Better handling of credentials
1. Make better connection between state and workunit
1. Ensure Docker is pulled if not exist

## Required

- Docker
- Terraform
- AWS credentials
- WESM and States downloaded

## WESM location

```
curl https://rockyweb.usgs.gov/vdelivery/Datasets/Staged/Elevation/metadata/WESM.gpkg --output data/WESM.gpkg
```

## US States file location

https://www.sciencebase.gov/catalog/item/52c78623e4b060b9ebca5be5

## USGS Point Cloud Data

```
https://registry.opendata.aws/usgs-lidar/
```

UnZip and place at `data/us-states.gpkg`

## Basic Method

Clean broken geometries, remove slivers, fill interior rings
```
make clean-wesm
```

Method to intersect WESM with individual states
```
make state-intersect
```

Method to index workunit by state
```
make wesm-index workunit=CA_SoCal_Wildfires_B2_2018 state=California
```