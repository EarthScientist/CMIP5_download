##########################################################################################################################################
# ESGF_Downloader.py
# author: Michael Lindgren (malindgren@alaska.edu)
# Version 2.0 - 02.15.2013
# 	 Important to note that the server can only return 10,000 records in a single file so if you are trying to access a lot of data
#    I would reccommend doing it in smaller subsets. i.e. dont download ALL MODELS at a time

# some examples of constructing the wget call to the portal
# http://esg-datanode.jpl.nasa.gov/esg-search/wget
# http://esg-datanode.jpl.nasa.gov/esg-search/wget?offset=300&limit=100
# http://pcmdi9.llnl.gov/esg-search/wget?variable=air_temperature&experiment=decadal2000&project=CMIP5
# http://pcmdi9.llnl.gov/esg-search/wget?variable=air_temperature&experiment=decadal2000&project=CMIP5

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# this is the openID I use without my actual username/password	#
# OPENID: https://www.earthsystemgrid.org/myopenid/<username> 	#
# PWD: 															#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

##########################################################################################################################################
import os, sys, re, glob, urllib2, time

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
wgetPath = "/big_storage/malindgren/wget"
dataPath = "/big_storage/malindgren/data"

# some time work for the log file name
t = time.asctime()
t = t.split(" ")

outFile = open(os.path.join(wgetPath,"LOG_FILE_ESGF_DOWNLOADER_"+t[1]+"_"+t[2]+"_"+t[4]+"_"+t[3].replace(":","")+".txt"),'a')

# this if/else loop is looking to see if the user has commented out the models line
if "models" in locals():
	for model in models:
		for experiment in experiments:
			for time_frequency in time_frequencies:
				for realm in realms:
					for CMOR_table in CMOR_tables:
						for ensemble in ensembles:
							for variable in variables:
								# here we create the new url name to generate the wget script needed to harvest the data
								new_url=base_url+"&model="+model+"&"+"experiment="+experiment+"&"+"time_frequency="+time_frequency+"&"+"realm="+realm+"&"+"cmor_table="+CMOR_table+"&"+"ensemble="+ensemble+"&"+"variable="+variable+"&"+"project=CMIP5"+"&"+"latest=true"

								response = urllib2.urlopen(new_url)
								
								print "creating wget script for url: " + new_url

								try:
									# Open our local file for writing
									local_file = open(os.path.join(wgetPath,model+'_'+variable+'_'+experiment+"_"+time_frequency+"_"+realm+'_'+CMOR_table+'_'+ensemble+'.sh'), "wt")
								
									# write to our local file
									local_file.write(response.read())
									local_file.close()

									# create a path variable that creates the output directory
									pathVarOut=os.path.join(dataPath,time_frequency,experiment,variable,ensemble)

									if os.path.isdir(pathVarOut) == False:
										os.makedirs(pathVarOut)
										os.chdir(pathVarOut) 

									# this line will initiate the script and it should bring up a java applet for login.
									os.system('bash '+os.path.join(wgetPath,model+'_'+variable+'_'+experiment+"_"+time_frequency+"_"+realm+'_'+CMOR_table+'_'+ensemble+'.sh'))
								except:
									# log the issue
									outFile.write(new_url+"\n")
									# continue on through the loop
									continue
else: # here we loop through the data where the user has commented out the models variable at the top of the script
	for experiment in experiments:
		for time_frequency in time_frequencies:
			for realm in realms:
				for CMOR_table in CMOR_tables:
					for ensemble in ensembles:
						for variable in variables:
							# here we create the new url name to generate the wget script needed to harvest the data
							new_url=base_url+"experiment="+experiment+"&"+"time_frequency="+time_frequency+"&"+"realm="+realm+"&"+"cmor_table="+CMOR_table+"&"+"ensemble="+ensemble+"&"+"variable="+variable+"&"+"project=CMIP5"+"&"+"latest=true"

							response = urllib2.urlopen(new_url)
							
							print "creating wget script for url: " + new_url

							try:
								# Open our local file for writing
								local_file = open(os.path.join(wgetPath,variable+'_'+experiment+"_"+time_frequency+"_"+realm+'_'+CMOR_table+'_'+ensemble+'.sh'), "wt")
							
								#Write to our local file
								local_file.write(response.read())
								local_file.close()

								# create a path variable that creates the output directory
								pathVarOut=os.path.join(downPath,time_frequency,experiment,variable,ensemble)

								if os.path.isdir(pathVarOut) == False:
									os.makedirs(pathVarOut)
									os.chdir(pathVarOut) 

								# this line will initiate the script and it should bring up a java applet for login.
								os.system('bash '+os.path.join(wgetPath,variable+'_'+experiment+"_"+time_frequency+"_"+realm+'_'+CMOR_table+'_'+ensemble+'.sh'))

							except:
								# log the issue
								outFile.write(new_url+"\n")
								# continue on through the loop
								continue
outFile.close()
