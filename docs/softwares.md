# Install required softwares and Python modules in Ubuntu 14.04

All following commands are run using the shell. Ubuntu 14.04 is used that has Python 3.4 installed.  

##Contents:
1. [Update/Upgrade the system](#1)
2. [Install spatial libraries](#2)
3. [Install Python related libraries and modules](#3)
4. [Install Postgres and PostGIS](#4)
5. [Next steps](#5)

## <a name="1"></a>1. Update / upgrade system:
>    sudo apt-get upgrade

>    sudo apt-get update

## <a name="2"></a>2. Install spatial libraries:
>   sudo apt-get install binutils libproj-dev gdal-bin python3-gdal libgdal-dev

## <a name="3"></a>3. Python

**Install Python related libraries**
>   sudo apt-get install python3-pip python-setuptools python-dev libevent-dev gfortran libopenblas-dev liblapack-dev libfreetype6-dev libxft-dev unzip

**Install required Python modules**
>   sudo pip3 install numpy psycopg2 python-dateutil pytz pyproj pandas geopandas shapely Fiona

>   sudo pip3 install tweepy flickrapi python-instagram

_Pip3 does not work properly after installing tweepy --> reinstall:_
>   sudo easy_install3 -U pip

**Test that Python and the modules are working properly**

Start python and try importing required modules (everything is working if errors are not occurring):
>   $python3 
>   > import geopandas, fiona, psycopg2, shapely, pytz, numpy, tweepy, instagram, pyproj

_Exit Python by CNTRL + C._

## <a name="4"></a>4. Postgres / PostGIS
>   apt-get install postgresql-9.4-postgis-2.1

## <a name="5"></a>5. Next steps
After successful installation of required libraries and Python modules it is time to [configure Postgres/PostGIS database](postgres_config.md).
