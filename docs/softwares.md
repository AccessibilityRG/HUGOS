# Install required softwares and Python modules in Ubuntu 14.04

All following commands are run using the shell. Ubuntu 14.04 is used that has Python 3.4 installed.  

#### Update / upgrade system:
>    sudo apt-get upgrade

>    sudo apt-get update


#### Install spatial libraries:
>   sudo apt-get install binutils libproj-dev gdal-bin python3-gdal libgdal-dev


#### Install Python related libraries
>   sudo apt-get install python3-pip python-setuptools python-dev libevent-dev gfortran libopenblas-dev liblapack-dev libfreetype6-dev libxft-dev unzip

#### Install required Python modules
>   sudo pip3 install numpy psycopg2 python-dateutil pytz pyproj pandas geopandas shapely Fiona

>   sudo pip3 install tweepy flickrapi python-instagram

##### Pip3 does not work properly after installing tweepy --> reinstall:
>   sudo easy_install3 -U pip

#### Test that Python and the modules are working properly

Start python:
>   python3 

Try importing required modules:
>   import geopandas, fiona, psycopg2, shapely, pytz, numpy, tweepy, instagram, pyproj

Exit Python by CNTRL + C
