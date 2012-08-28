import os, sys, re, glob, urllib2, time
# http://esg-datanode.jpl.nasa.gov/esg-search/wget
# http://esg-datanode.jpl.nasa.gov/esg-search/wget?offset=300&limit=100
# http://pcmdi9.llnl.gov/esg-search/wget?variable=air_temperature&experiment=decadal2000&project=CMIP5
# http://pcmdi9.llnl.gov/esg-search/wget?variable=air_temperature&experiment=decadal2000&project=CMIP5

# OPENID: https://www.earthsystemgrid.org/myopenid/EarthScientist
# PWD: 7570483

# this will collect the time variable.  only partially working at the moment
# # # # # # # # # # # # # # # # # # # # #
in_localtime=time.localtime(time.time())#
in_localtime2=time.asctime()			#
# # # # # # # # # # # # # # # # # # # # #

# variable names
experiments = ["historical","rcp26","rcp45","rcp60","rcp85"]
time_frequencies = ["mon"] 
realms = ["atmos"] 
CMOR_tables = ["Amon"] 
ensembles = ["r1i1p1"] 
variables = ["tas","tasmin","tasmax","pr","psl","uas","vas","sfcWind","tauu","tauv","ua","va","hur","hurs","hus","huss","rsds","clt","sit","sic"]

# this is the name or the list of names that the search will query on.  I am beginning with this one.
base_url="http://pcmdi9.llnl.gov/esg-search/wget?"
outPath="/workspace/Shared/Michael/CMIP5/WGET_DOWNLOAD_28Aug2012/wget"
downPath="/workspace/Shared/Michael/CMIP5/WGET_DOWNLOAD_28Aug2012"

response = urllib2.urlopen(base_url)

# this is the new log file that will list any download issues encountered from the wget fownload 
dateTime=str(in_localtime[1])+"_"+str(in_localtime[2])+"_"+str(in_localtime[0])+"_"+str(in_localtime[3])+str(in_localtime[4])+str(in_localtime[5])
if os.path.exists(os.path.join(outPath,'wgetLogFile_'+dateTime+'.txt')) == False:
	outFile1=open(os.path.join(outPath,'wgetLogFile_'+dateTime+'.txt'),'a')
else:
	os.remove(os.path.join(outPath,'wgetLogFile_'+dateTime+'.txt'))
	outFile1=open(os.path.join(outPath,'wgetLogFile_'+dateTime+'.txt'),'a')


# loop through all of the aspects of the naming convention for each var
for experiment in experiments:
	for time_frequency in time_frequencies:
		for realm in realms:
			for CMOR_table in CMOR_tables:
				for ensemble in ensembles:
					for variable in variables:
						# here we create the new url name to generate the wget script needed to harvest the data
						new_url=base_url+"experiment="+experiment+"&"+"time_frequency="+time_frequency+"&"+"realm="+realm+"&"+"cmor_table="+CMOR_table+"&"+"ensemble="+ensemble+"&"+"variable="+variable+"&"+"project=CMIP5"

						response = urllib2.urlopen(new_url)
						
						print "creating wget script for url: " + new_url

						try:
							# Open our local file for writing
							local_file = open(os.path.join(outPath,variable+'_'+experiment+"_"+time_frequency+"_"+realm+'_'+CMOR_table+'_'+ensemble+'.sh'), "wt")
							#Write to our local file
							local_file.write(response.read())
							local_file.close()

							# this line will initiate the script and it should bring up a java applet for login.
							#os.system('bash '+os.path.join(outPath,variable+'_'+experiment+"_"+time_frequency+"_"+realm+'_'+CMOR_table+'_'+ensemble+'.sh'))
						except:
							outFile1.write(new_url+"\n")
							continue
# close that wget log file
outFile1.close()


# this is the 
dateTime=str(in_localtime[1])+"_"+str(in_localtime[2])+"_"+str(in_localtime[0])+"_"+str(in_localtime[3])+str(in_localtime[4])+str(in_localtime[5])
if os.path.exists(os.path.join(outPath,'wgetLogFile_'+dateTime+'.txt')) == False:
	outFile2=open(os.path.join(outPath,'wgetLogFile_'+dateTime+'.txt'),'a')
else:
	os.remove(os.path.join(outPath,'wgetLogFile_'+dateTime+'.txt'))
	outFile2=open(os.path.join(outPath,'wgetLogFile_'+dateTime+'.txt'),'a')


# here we list the files that were downloaded in the previous loop.
filelist=glob.glob(os.path.join(outPath,"*.sh"))
for f in filelist:
	# create a path variable that creates the output directory
	pathVarOut=os.path.join(downPath,time_frequency,experiment,variable,ensemble)
	
	try:
		if os.path.isdir(pathVarOut) == True:
			print "  outputting to:", pathVarOut
		else:
			os.makedirs(pathVarOut)
			os.chdir(pathVarOut) # change this to the working dir that we want the data to be output to
			os.system("chmod -x "+f) # then we want to change the mode of the file to be exe
			os.system(". "+f)
	except:
		# log the filename that is giving errors
		outFile2.write(f+"\n")
		continue

outFile2.close()
