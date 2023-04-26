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

1. The current method is too slow for launching the EC2.  Time is taken up in pulling the needed Docker. Ideally, replaction of the server would suffice.
1. The full WESM file is a very slow read for the process.  A method to reduce the file size of the WESM and target on a state by state region is being explored   
1. Better handling of credentials

## Required

- Docker
- Terraform
- AWS credentials

## WESM location

```
curl https://rockyweb.usgs.gov/vdelivery/Datasets/Staged/Elevation/metadata/WESM.gpkg --output data/WESM.gpkg
```

## USGS Data

```
https://registry.opendata.aws/usgs-lidar/
```

