# HUGOS - Geosocial observation system (University of Helsinki)

HUGOS is a selection of tools to collect and manage (geo)social media data from different social media platforms such as Twitter and Instagram (these two at the moment). 
Tools are programmed in Python and Postgres/PostGIS is used as a backend for storing the data and controlling the data collection process.

It is possible to collect the data using multiple servers simultaneously while controlling everything from a single Postgres table. 
 
## [Installations & Configurations](docs/Install_readme.md)
Setting up a (Linux Ubuntu) server and installing necessary softwares. Configuring PostGIS database for data collection.

## HUGOS consist of the following tools:

### [HUGOS-Instagram](HUGOS-Instagram)
HUGOS-Instagram is a tool for collecting Instagram data into PostGIS database.

### [HUGOS-Twitter](HUGOS-Twitter)
HUGOS-Twitter is a tool for collecting Twitter data into PostGIS database.

### AWS-tools
Convenience scripts for working with Amazon Web Services (e.g. creating new instances etc.) 

