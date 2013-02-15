import os, re, sys, ftplib, time
from ftplib import FTP

# # # # # # # # # # # # # # # # # # # # 
in_localtime=time.localtime(time.time())#
in_localtime2=time.asctime()
# # # # # # # # # # # # # # # # # # # # 
##################################################
# PATHS
outputRootDir = "/workspace/Shared/Michael/CMIP5/download2/"
##################################################

# this section of the script can be modified to get to different levels within the directory structure
product = ['output1'] # this can be output1 or output2
institutions = [] #  SEE BELOW ftp.nlst("/"+product+)# this can be a list of desired groups or it can be 
models = [] # SEE BELOW ["BNU"] # [here we weant to have something related to the listing of the dirs] this can be a list or it can be the list of all availabe
experiments = ["historical","rcp45","rcp60","rcp85"]
time_frequency = ["mon"] # this can be mon, day
realm = ["atmos"] # this is the realm of data we are constantly looking at
CMOR_table = ["Amon"] # when dealing with monthlies this is the value.  not sure about the dailies
ensembles = ["r1i1p1"] # there are many realization physics.  I have only downloaded the first one thus far
variables = ["tas","tasmin","tasmax","pr","psl","uas","vas","sfcWind","tauu","tauv","ua","va","hur","hurs","hus","huss","rsds","clt"]
file_version = ["1"]

# # This is added for this version of the code, but is not yet fully implemented. [ML needs to add functionality]
# # a simple class with a write method
# class WritableObject:
#     def __init__(self):
#         self.content = []
#     def write(self, string):
#         self.content.append(string)
# ###### <<< ----------------- >>> ######

#####################################################################
# This is where it is necessary to put in the name of the ftp server 
#  in the case of this script at the moment it is built to download 
#  the data from the CMIP5 ftp server.
ftp = FTP('cmip5.llnl.gov')
print ftp.login('EarthScientist', '7570483')
#####################################################################

print "# # # # # # # # #  WELCOME MESSAGE FROM SERVER # # # # # # # # # "
print ftp.getwelcome()
print "# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #"


# ################################################################################################
# # this little function checks to see if a given subdirectory exists within the remote directory 
# def checkifexists(pathVar):
#     filelist = [] #to store all files
#     filelist = ftp.nlst()    # append to list  
#     for f in filelist:
#         if pathVar in f:
#             return 1
#         else:
#             print "model path does not exist ... next model."
#             #do your processing here
#             return 0
# ################################################################################################
# # this instantiates a writer object that will record what happens
# outReport = WritableObject()
# sys.stdout = outReport

dateTime=str(in_localtime[1])+"_"+str(in_localtime[2])+"_"+str(in_localtime[0])+"_"+str(in_localtime[3])+str(in_localtime[4])+str(in_localtime[5])
if os.path.exists(os.path.join(outputRootDir,'logFile_'+dateTime+'.txt')) == False:
	outFile=open(os.path.join(outputRootDir,'logFile_'+dateTime+'.txt'),'a')
else:
	os.remove(os.path.join(outputRootDir,'logFile_'+dateTime+'.txt'))
	outFile=open(os.path.join(outputRootDir,'logFile_'+dateTime+'.txt'),'a')

#pathList=[]
for p in product:
	pp=os.path.basename(p)
	institutions = ftp.nlst("/"+pp+"/") # get the basenames of the institutions
	for i in institutions:
		ii=os.path.basename(i)
		models = ftp.nlst("/"+pp+"/"+ii+"/") # get the basename of the models...
		for m in models:
			mm=os.path.basename(m)
			for e in experiments:
				for t in time_frequency:
					for r in realm:
						for c in CMOR_table:
							# list the ensembles
							ensembles = ftp.nlst("/"+pp+"/"+ii+"/"+mm+"/"+e+"/"+t+"/"+r+"/"+c+"/")
							nvars = len(ensembles)
							en_list=[]
							length_list=[]
							for en in range(0,nvars):
								en_cur = os.path.basename(ensembles[en])
								# for jj in range(0,length(ensembles))
								# this will set a variable dynamically in Python
								# create an empy list with the dynamic name
								exec 'en_%s = []' % str(en) # this works!
								
								#this lists all available variables and sees if the one we are looking for even exists.
								varCheck = ftp.nlst(ensembles[en])
								for v in variables:
									exec 'en_list.append("en_%d")' % en
									if v in varCheck:
										for f in file_version:
											unique_path="/"+pp+"/"+ii+"/"+mm+"/"+e+"/"+t+"/"+r+"/"+c+"/"+en_cur+"/"+v+"/"+f+"/"
											# fill that list wth te dynamic name
											exec 'en_%d.append(ftp.nlst(unique_path))' % en
								exec 'length_list.append(len(en_%d))' % en
							
							# compare the outputs of the n ensembles and grab the one with the most files listed.
							# NOT WORKING!
							maxNfiles=length_list.index(max(length_list))

							for d in vars()[en_list[maxNfiles]]):
								try:
									print "  Downloading: ",d

									#########################################################
									# THIS IS FOR THE OUTPUT FILES
									# This checks the existence of a given directory
									#  and will recurively create what it needs to
									#  fit the new directory leaf.
									dd=d.split("/")
									pathVarOut = os.path.join(outputRootDir,dd[4],dd[9])
									
									if os.path.exists(os.path.join(pathVarOut,os.path.basename(d))) == False:
										if os.path.isdir(pathVarOut) == True:
											print "  outputting to:", pathVarOut
										else:
											os.makedirs(pathVarOut)
									#########################################################
										local_filename = os.path.join(pathVarOut, d.rpartition("/")[len(d.rpartition("/"))-1])
										# lf = open(local_filename, "wb")
										ftp.retrbinary('RETR ' + d, open(local_filename,'wb').write)
										print " completed: ", time.asctime()
								except:
									print "skipping..."
									#outFile.write(d+"\n")
									continue

							# this is just a little thing to check if a given varname exists in the locals() and if it does, it deletes it (not working.)
							this = sys.modules[__name__]
							for n in en_list:
							   if n[0]!='_': delattr(this, n)




