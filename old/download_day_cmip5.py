import os, sys, re, glob, csv, time

outPath="/scratch/malindgren/CMIP5/data"
# list the files CCSM4_pr_historical_day_atmos_day_r2i1p1
files=glob.glob("/scratch/malindgren/CMIP5/wget/*historical*day*.sh")

for f in files:
	try:
		f1=f.split("/")
		f2=f1[len(f1)-1].split("_")
		newPath=os.path.join(outPath,f2[3],f2[2],f2[1])
		
		if os.path.exists(newPath)==False:
			os.makedirs(newPath)
		
		os.chdir(newPath)
		print "runnning wget_file:",f
		os.system('bash '+f)

		