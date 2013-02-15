# config file 
# this is a python list of the model(s) you are looking to download

###################################
# this base_url does not need to change it is the base portal from the PCMDI Group
base_url = "http://pcmdi9.llnl.gov/esg-search/wget?distrib=true"
###################################

# these are variables that would need to be updated depending on what you are trying to harvest
models = ["MRI-CGCM3","GISS-E2-R","GFDL-CM3","IPSL-CM5A-LR","CCSM4"]
experiments = ["rcp45","rcp60","rcp85"]
time_frequencies = ["day"]
realms = ["atmos"]
CMOR_tables = ["day"]
ensembles = ["r1i1p1"]
variables = ["uas","vas","tas","pr","psl"]

# these are some path variables specific to where you want the data to go
# in your local file system
wgetPath = "/big_storage/malindgren/wget/wget_day_nov2012"
dataPath = "/big_storage/malindgren/data/data_day_nov2012"
