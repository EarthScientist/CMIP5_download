import os, sys, re, glob, urllib2, time

# some examples of constructing the wget call to the portal
# http://esg-datanode.jpl.nasa.gov/esg-search/wget
# http://esg-datanode.jpl.nasa.gov/esg-search/wget?offset=300&limit=100
# http://pcmdi9.llnl.gov/esg-search/wget?variable=air_temperature&experiment=decadal2000&project=CMIP5
# http://pcmdi9.llnl.gov/esg-search/wget?variable=air_temperature&experiment=decadal2000&project=CMIP5

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# this is the openID I use without my actual username/password	#
# OPENID: https://www.earthsystemgrid.org/myopenid/				#
# PWD: 															#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# this will collect the time variable.  only partially working at the moment -- mainly for log file naming
# # # # # # # # # # # # # # # # # # # # #
in_localtime=time.localtime(time.time())#
in_localtime2=time.asctime()			#
# # # # # # # # # # # # # # # # # # # # #

# variable names
models=["CCSM4","GFDL-CM3","CNRM-CM5","IPSL-CMA5-LR","MPI-ESM-LR","MRI-CGCM3","GISS-E2-R"] # if all models want to be accessed simply comment this line out
experiments = ["historical","rcp26","rcp45","rcp60","rcp85"]
time_frequencies = ["day"]
realms = ["atmos"]
CMOR_tables = ["day"] 
ensembles = ["r1i1p1","r2i1p1","r3i1p1"] 
variables = ["tas","tasmin","tasmax","pr","psl","uas","vas","sfcWind","ua","va"]

# this is the name or the list of names that the search will query on.  I am beginning with this one.
base_url="http://pcmdi9.llnl.gov/esg-search/wget?"
outPath="/workspace/Shared/Michael/CMIP5/WGET_DOWNLOAD_28Aug2012/wget"
downPath="/workspace/Shared/Michael/CMIP5/WGET_DOWNLOAD_28Aug2012/data"

response = urllib2.urlopen(base_url)

# this is the new log file that will list any download issues encountered from the wget download 
dateTime=str(in_localtime[1])+"_"+str(in_localtime[2])+"_"+str(in_localtime[0])+"_"+str(in_localtime[3])+str(in_localtime[4])+str(in_localtime[5])
if os.path.exists(os.path.join(outPath,'wgetLogFile_'+dateTime+'.txt')) == False:
	outFile=open(os.path.join(outPath,'wgetLogFile_'+dateTime+'.txt'),'a')
else:
	os.remove(os.path.join(outPath,'wgetLogFile_'+dateTime+'.txt'))
	outFile=open(os.path.join(outPath,'wgetLogFile_'+dateTime+'.txt'),'a')

# this if/else loop is looking to see if the user has commented out the models line
if "models" in locals():
	# loop through all of the aspects of the naming convention for each var
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
								
								# here we write out the response to a new file
								# Open our local file for writing
								local_file = open(os.path.join(outPath,model+'_'+variable+'_'+experiment+"_"+time_frequency+"_"+realm+'_'+CMOR_table+'_'+ensemble+'.sh'), "w")
							
								#Write to our local file
								local_file.write(response.read())
								#local_file.close()

								print "response written to file."

								try:
									# the new lines file
									lines=open(os.path.join(outPath,model+'_'+variable+'_'+experiment+"_"+time_frequency+"_"+realm+'_'+CMOR_table+'_'+ensemble+'.sh'),'r')

									print "file read back in..."
									#create an empty list object
									lineList=[]

									# here we find out the line numbers of the lines in the file containing ".nc'"
									# lOOP THORUGH THE LIST: (where i is line_number)
									for i, line in enumerate(lines):
										pattern = re.compile(".nc'") # looking for the lines with the .nc' in the line.  this will indicate the ones we want
										if pattern.search(line):
											#print i, lines[i]
											lineList.append(i)
									if len(lineList) > 0:
										print "listing and running the wget commands for .nc downloads..."
										for l in lineList:	
											if os.path.exists(os.path.join(pathVarOut,lines[l]))==True:
												if os.path.getsize(os.path.join(pathVarOut,lines[l])) <= 1:
													
													print lines[l]
													
													beginLine=min(lineList)
													endLine=max(lineList)

													wget_new_part1 = lines[0:beginLine]
													wget_new_part2 = lines[endLine+1:i]

													new_wget_file=open('/workspace/Shared/Michael/CMIP5/WGET_DOWNLOAD_28Aug2012/wget/tempDir/tmp'+count+'.sh','w')
													#write the new wget file with one var
													for w in lines[0:beginLine]:
														new_wget_file.write(w)
													new_wget_file.write(lines[l])
													for w in lines[endLine+1:i]:
														new_wget_file.write(w)
														pathVarOut=os.path.join(downPath,time_frequency,experiment,variable,ensemble)
													new_wget_file.close()
													if os.path.isdir(pathVarOut) == True:
														print "  outputting to:", pathVarOut
													else:
														os.makedirs(pathVarOut)
														os.chdir(pathVarOut) # change this to the working dir that we want the data to be output to
													
													# this line will initiate the script and it should bring up a java applet for login.
													os.system('bash '+'/workspace/Shared/Michael/CMIP5/WGET_DOWNLOAD_28Aug2012/wget/tempDir/tmp_'+count+'.sh -i')	
											else:
												beginLine=min(lineList)
												endLine=max(lineList)

												wget_new_part1 = lines[0:beginLine]
												wget_new_part2 = lines[endLine+1:i]

												new_wget_file=open('/workspace/Shared/Michael/CMIP5/WGET_DOWNLOAD_28Aug2012/wget/tempDir/tmp_'+dateTime+'.sh','w')
												#write the new wget file with one variable
												for w in lines[0:beginLine]:
													new_wget_file.write(w)
												new_wget_file.write(lines[l])
												for w in lines[endLine+1:i]:
													new_wget_file.write(w)
													pathVarOut=os.path.join(downPath,time_frequency,experiment,variable,ensemble)
												new_wget_file.close()
												if os.path.isdir(pathVarOut) == True:
													print "  outputting to:", pathVarOut
												else:
													os.makedirs(pathVarOut)
													os.chdir(pathVarOut) # change this to the working dir that we want the data to be output to
												
												# this line will initiate the script and it should bring up a java applet for login.
												os.system('bash '+'/workspace/Shared/Michael/CMIP5/WGET_DOWNLOAD_28Aug2012/wget/tempDir/tmp_'+dateTime+'.sh -i')
								except:
									# log the issue
									outFile.write(new_url+"\n")
									# continue on through the loop
									#continue


									#####

else: # here we loop through the data where the user has commented out the models variable at the top of the script
	for experiment in experiments:
		for time_frequency in time_frequencies:
			for realm in realms:
				for CMOR_table in CMOR_tables:
					for ensemble in ensembles:
						for variable in variables:
							# here we create the new url name to generate the wget script needed to harvest the data
							new_url=new_url=base_url+"experiment="+experiment+"&"+"time_frequency="+time_frequency+"&"+"realm="+realm+"&"+"cmor_table="+CMOR_table+"&"+"ensemble="+ensemble+"&"+"variable="+variable+"&"+"project=CMIP5"+"&"+"latest=true"
							response = urllib2.urlopen(new_url)
							print "creating wget script for url: " + new_url

							try:
								
								# Open our local file for writing
								local_file = open(os.path.join(outPath,model+'_'+variable+'_'+experiment+"_"+time_frequency+"_"+realm+'_'+CMOR_table+'_'+ensemble+'_'+dateTime+'.sh'), "wt")
							
								#Write to our local file
								local_file.write(response.read())
								local_file.close()

								lines=open(os.path.join(outPath,model+'_'+variable+'_'+experiment+"_"+time_frequency+"_"+realm+'_'+CMOR_table+'_'+ensemble+'_'+dateTime+'.sh'),'r')

								#create an empty list object
								lineList=[]
						
								# lOOP THORUGH THE LIST: (where i is line_number)
								for i, line in enumerate(lines):
									pattern = re.compile(".nc'") # looking for the lines with the .nc' in the line.  this will indicate the ones we want
									if pattern.search(line):
										print i, lines[i]
										lineList.append(i)
								if len(lineList) != 0:
									print "listing and running the wget commands for .nc downloads..."
									for l in lineList:	
										print l	
										if os.path.exists(os.path.join(pathVarOut,lines[l]))==True:
											if os.path.getsize(os.path.join(pathVarOut,lines[l])) <= 1:
												
												print lines[l]

												beginLine=min(lineList)
												endLine=max(lineList)

												wget_new_part1 = lines[0:beginLine]
												wget_new_part2 = lines[endLine+1:i]

												new_wget_file=open('/workspace/Shared/Michael/CMIP5/WGET_DOWNLOAD_28Aug2012/wget/tempDir/tmp_'+dateTime+'.sh','w')
												#write the new wget file with one var
												for w in lines[0:beginLine]:
													new_wget_file.write(w)
												new_wget_file.write(lines[l])
												for w in lines[endLine+1:i]:
													new_wget_file.write(w)
													pathVarOut=os.path.join(downPath,time_frequency,experiment,variable,ensemble)
												new_wget_file.close()
												if os.path.isdir(pathVarOut) == True:
													print "  outputting to:", pathVarOut
												else:
													os.makedirs(pathVarOut)
													os.chdir(pathVarOut) # change this to the working dir that we want the data to be output to
												
												# this line will initiate the script and it should bring up a java applet for login.
												os.system('bash '+'/workspace/Shared/Michael/CMIP5/WGET_DOWNLOAD_28Aug2012/wget/tempDir/tmp_'+dateTime+'.sh -i')
													
												
										else:
											beginLine=min(lineList)
											endLine=max(lineList)

											wget_new_part1 = lines[0:beginLine]
											wget_new_part2 = lines[endLine+1:i]

											new_wget_file=open('/workspace/Shared/Michael/CMIP5/WGET_DOWNLOAD_28Aug2012/wget/tempDir/tmp_'+dateTime+'.sh','w')
											#write the new wget file with one var
											for w in lines[0:beginLine]:
												new_wget_file.write(w)
											new_wget_file.write(lines[l])
											for w in lines[endLine+1:i]:
												new_wget_file.write(w)
												pathVarOut=os.path.join(downPath,time_frequency,experiment,variable,ensemble)
											new_wget_file.close()
											if os.path.isdir(pathVarOut) == True:
												print "  outputting to:", pathVarOut
											else:
												os.makedirs(pathVarOut)
												os.chdir(pathVarOut) # change this to the working dir that we want the data to be output to
											
											# this line will initiate the script and it should bring up a java applet for login.
											os.system('bash '+'/workspace/Shared/Michael/CMIP5/WGET_DOWNLOAD_28Aug2012/wget/tempDir/tmp_'+dateTime+'.sh -i')
							except:
								# log the issue
								outFile.write(new_url+"\n")
								# continue on through the loop
								continue
# close that wget log file
outFile.close()
