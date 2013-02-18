CMIP5_download
==============

This script (ESGF_Downloader_v2.py) is useful for downloading large amounts of IPCC climate data from the AR5 report's data portal hosted by PCMDI at llnl.gov.  The script requires some inputs which will be described below.  The most important being the Username and Password for a portal in the Earth System Grid Federation, which can be created at: https://pcmdi9.llnl.gov/esgf-web-fe/createAccount

The variables that will need adjusting for the data the user wants to access is as follows:

# ALL OF THESE VARIABLES ARE PYTHON LISTS [] even if it is a list of only one element!!!!

models = [list of the desired model names] >>example>> ["MRI-CGCM3","GISS-E2-R","GFDL-CM3","IPSL-CM5A-LR","CCSM4"]
experiments = [list of the desired experiments] >>example>> ["rcp45","rcp60","rcp85"]
time_frequencies = [list of the desired time frequencies] >>example>> ["day"]
realms = [list of the desired realms] >>example>> ["atmos"]
CMOR_tables = [list of the desired CMOR tables] >>example>> ["day"]
ensembles = [list of the desired ensembles] >>example>> ["r1i1p1"]
variables = [list of the desired variables] >>example>> ["uas","vas","tas","pr","psl"]

# these are some path variables specific to where you want the data to go
# in your local file system
wgetPath = this is the path to the folder where you want to download and store the wget scripts >>example>> "/big_storage/malindgren/wget"
dataPath = this is the path to the folder where you want to download and store the data files  >>example>> "/big_storage/malindgren/data"

Discover the desired names of the above variables from the ESGF Web Portal GUI, located at: http://pcmdi9.llnl.gov/esgf-web-fe/live
