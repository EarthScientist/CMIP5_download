##########################################################################################################################################
# ESGF_Downloader.py
# author: Michael Lindgren (malindgren@alaska.edu)
# Version 2.0 - 02.15.2013
# 	Script can be loaded at the command line and given the ESGF_config.py file, which has been modified by the user
#    to get the data they desire. 
# 	 Important to note that the server can only return 10,000 records in a single file so if you are trying to access a lot of data
#    I would reccommend doing it in smaller subsets. i.e. dont download ALL MODELS at a time
##########################################################################################################################################

def harvestData(configFile):
	'''function to harvest PCMDI Data'''
	import os, sys, re, glob, urllib2, time
	from configFile import *
	#response = urllib2.urlopen(base_url)
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
									new_url=base_url+"model="+model+"&"+"experiment="+experiment+"&"+"time_frequency="+time_frequency+"&"+"realm="+realm+"&"+"cmor_table="+CMOR_table+"&"+"ensemble="+ensemble+"&"+"variable="+variable+"&"+"project=CMIP5"+"&"+"latest=true"

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
										os.system('bash '+os.path.join(dataPath,model+'_'+variable+'_'+experiment+"_"+time_frequency+"_"+realm+'_'+CMOR_table+'_'+ensemble+'.sh'))
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
									os.system('bash '+os.path.join(downPath,variable+'_'+experiment+"_"+time_frequency+"_"+realm+'_'+CMOR_table+'_'+ensemble+'.sh'))

								except:
									# log the issue
									outFile.write(new_url+"\n")
									# continue on through the loop
									continue
	return
