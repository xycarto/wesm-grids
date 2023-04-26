FROM ubuntu:22.04

ENV TZ Pacific/Auckland

RUN apt-get update
RUN apt-get install -y tzdata
RUN echo "Pacific/Auckland" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata

RUN apt-get update &&  \
    apt-get install -y --no-install-recommends gnupg ca-certificates software-properties-common dirmngr wget \
    curl git-core libssl-dev libssh2-1-dev libcurl4-openssl-dev libxml2-dev && \
    apt upgrade --yes && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install pip3 and compilation tools
RUN apt-get update && \
	apt-get install -y python3-pip cmake++ ninja-build && \
    apt upgrade --yes && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
RUN pip3 install Ninja

# Install GDAL
RUN apt-get update && \
	apt-get install -y gdal-bin libgdal-dev && \
    apt upgrade --yes && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Compile LASzip
RUN cd / && git clone --depth 1 https://github.com/LASzip/LASzip.git
RUN cd /LASzip && mkdir build && cd build && cmake -G Ninja ../ && ninja && ninja install && cd /

# Compile PDAL
RUN cd / && git clone --depth 1 https://github.com/pdal/pdal.git
RUN cd /pdal && mkdir build && cd build && cmake -G Ninja .. && \
    sed -i 's/CMAKE_BUILD_TYPE:STRING=/CMAKE_BUILD_TYPE:STRING=Release/' \
    ./CMakeCache.txt && echo 'WITH_LASZIP:BOOL=ON' >> ./CMakeCache.txt && ninja && ninja install && cd /

# Install Python packages
RUN pip3 install boto3 geopandas rasterio pyproj

RUN apt-get update && \
    apt-get install -y awscli
    
RUN pip3 install awscli --upgrade

