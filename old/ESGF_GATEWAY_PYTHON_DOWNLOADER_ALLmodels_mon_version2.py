import os, sys, re, glob, urllib2, time, csv

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
in_localtime2=time.asctime()		#
# # # # # # # # # # # # # # # # # # # # #

# variable names
#models=["MRI-CGCM3","GISS-E2-R","GFDL-CM3","CNRM-CM5","IPSL-CMA5-LR","MPI-ESM-LR","CCSM4"] # if all models want to be accessed simply comment this line out
experiments = ["historical"]#,"rcp26",
time_frequencies = ["mon"]
realms = ["atmos"] 
CMOR_tables = ["Amon"] 
ensembles = ["r1i1p1","r2i1p1"] 
variables = ["tas","pr","psl"]#,

# this is the name or the list of names that the search will query on.  I am beginning with this one.
base_url="http://pcmdi9.llnl.gov/esg-search/wget?"
outPath="/big_storage/malindgren"
downPath="/big_storage/malindgren"

response = urllib2.urlopen(base_url)

# this is the wget value that the pcmdi server is generating to actually download a given file
# I am going to create this thing and issue the command python instead of dealing with their never ending 
wget_command_credentials = "wget -v -c --ca-directory=/home/UA/malindgren/.esg/certificates --certificate=/home/UA/malindgren/.esg/credentials.pem --private-key=/home/UA/malindgren/.esg/credentials.pem --save-cookies=/home/UA/malindgren/.esg/cookies --load-cookies=/home/UA/malindgren/.esg/cookies"

# this is the new log file that will list any download issues encountered from the wget download 
dateTime=str(in_localtime[1])+"_"+str(in_localtime[2])+"_"+str(in_localtime[0])+"_"+str(in_localtime[3])+str(in_localtime[4])+str(in_localtime[5])
if os.path.exists(os.path.join(outPath,'wgetLogFile_'+dateTime+'.txt')) == False:
	outFile=open(os.path.join(outPath,'wgetLogFile_'+dateTime+'.txt'),'a')
else:
	os.remove(os.path.join(outPath,'wgetLogFile_'+dateTime+'.txt'))
	outFile=open(os.path.join(outPath,'wgetLogFile_'+dateTime+'.txt'),'a')
#open a csv writer
f=open(os.path.join("/scratch/malindgren/CMIP5/other","wget_masterTable_mon_sic.csv"),'w')
c = csv.writer(f)
lineList=[]

# this if/else loop is looking to see if the user has commented out the models line

for experiment in experiments:
        for time_frequency in time_frequencies:
                for CMOR_table in CMOR_tables:
                        for ensemble in ensembles:
                                for variable in variables:
                                        # here we create the new url name to generate the wget script needed to harvest the data
                                        new_url=base_url+"experiment="+experiment+"&"+"time_frequency="+time_frequency+"&"+"cmor_table="+CMOR_table+"&"+"ensemble="+ensemble+"&"+"variable="+variable+"&"+"project=CMIP5"+"&"+"latest=true"

                                        response = urllib2.urlopen(new_url)
                                        
                                        print "creating wget script for url: " + new_url

                                        try:
                                                # Open our local file for writing
                                                local_file = open(os.path.join(outPath,"wget",variable+'_'+experiment+"_"+time_frequency+"_"+CMOR_table+'_'+ensemble+'.sh'), "wt")
                                        
                                                #Write to our local file
                                                local_file.write(response.read())
                                                local_file.close()

                                                # create a path variable that creates the output directory
                                                # pathVarOut=os.path.join(downPath,time_frequency,experiment,variable,ensemble)

                                                # if os.path.isdir(pathVarOut) == True:
                                                # 	print "  outputting to:", pathVarOut
                                                # 	os.chdir(pathVarOut)
                                                # else:
                                                # 	os.makedirs(pathVarOut)
                                                # 	os.chdir(pathVarOut) # change this to the working dir that we want the data to be output to


                                                # wget_file=open(os.path.join(outPath,"seaice",variable+'_'+experiment+"_"+time_frequency+"_"+CMOR_table+'_'+ensemble+'.sh'), "rt")

                                                # # here we find out the line numbers of the lines in the file containing ".nc'"
                                                # # lOOP THORUGH THE LIST: (where i is line_number)
                                                # # wget_file=open("/workspace/Shared/Michael/CMIP5/WGET_DOWNLOAD_28Aug2012/wget2/MRI-CGCM3_ua_historical_mon_atmos_Amon_r2i1p1.sh",'rt')
                                                # #open a csv writer
                                                # #c = csv.writer(open(os.path.join("/scratch/malindgren/CMIP5/other","wget_masterTable_mon.csv"),'wt'))

                                                

                                                # # here we find out the line numbers of the lines in the file containing ".nc'"
                                                # # lOOP THORUGH THE LIST: (where i is line_number)
                                                # for i, line in enumerate(wget_file):
                                                #         #print i,line
                                                #         pattern = re.compile(".nc'") # looking for the lines with the .nc' in the line.  this will indicate the ones we want
                                                #         if pattern.search(line):
                                                #                 #keep appending the nc filenames from the list
                                                #                 lineList.append(pathVarOut+","+line.split()[1])

                                                #                 # write a new row in the damn csv
                                                #                 c.writerow([pathVarOut,line.split()[1]])
                                        
                                        except:
                                                continue
##f.close()
##
##try:
##f=open(os.path.join("/scratch/malindgren/CMIP5/other","wget_masterTable_mon_sic.csv"),'r')
##
##for i, line in enumerate(f):
##	pathVarOut=line.split(",")[0]
##
##	if os.path.isdir(pathVarOut) == True:
##		print "  outputting to:", pathVarOut
##		os.chdir(pathVarOut)
##	else:
##		os.makedirs(pathVarOut)
##		os.chdir(pathVarOut) # change this to the working dir that we want the data to be output to
##		split = line.split(",")
##
##	# this line will initiate the script and it should bring up a java applet for login.
##	os.system('wget '+wget_command_credentials+" "+split[1].strip('\r\n'))
##
##except:
##	# do some logging:
##	# log the issue
##	outFile.write(line+"\n")
##	# continue on through the loop
##	# pass to the next point in the loop
##	pass
##
