import os, sys, re, glob, csv, time

wget_command_credentials = "wget -v -c --ca-directory=/home/UA/malindgren/.esg/certificates --certificate=/home/UA/malindgren/.esg/credentials.pem --private-key=/home/UA/malindgren/.esg/credentials.pem --save-cookies=/home/UA/malindgren/.esg/cookies --load-cookies=/home/UA/malindgren/.esg/cookies"

try:
	f=open(os.path.join("/scratch/malindgren/CMIP5/other","wget_masterTable_mon.csv"),'r')

	for i, line in enumerate(f):
		pathVarOut=line.split(",")[0]

		if os.path.isdir(pathVarOut) == True:
			print "  outputting to:", pathVarOut
			os.chdir(pathVarOut)
		else:
			os.makedirs(pathVarOut)
			os.chdir(pathVarOut) # change this to the working dir that we want the data to be output to
		
		split = line.split(",")
		split_1 = split[1].strip('\r\n')
		split_2 = split_1.strip("'")

		# this line will initiate the script and it should bring up a java applet for login.
		os.system(wget_command_credentials+" "+split_2)

except:
	# do some logging:
	# log the issue
	outFile.write(line+"\n")
	# continue on through the loop
	# pass to the next point in the loop
	pass
