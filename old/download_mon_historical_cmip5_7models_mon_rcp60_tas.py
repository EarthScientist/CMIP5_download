import os, sys, re, glob, csv, time

outPath="/big_storage/malindgren/data"
os.chdir(outPath)
# list the files CCSM4_pr_historical_day_atmos_day_r2i1p1
files=glob.glob("/big_storage/malindgren/wget/wget_rcp60/*tas*.sh")

for f in files:
	try:
		f1=f.split("/")
		f2=f1[len(f1)-1].split("_")
		f3=f2[len(f2)-1]
		f4=f3.split(".")[0]
		newPath=os.path.join(outPath,f2[3],f2[2],f2[1],f4)
		
		if os.path.isdir(newPath)==False:
			os.makedirs(newPath)
		
		os.chdir(newPath)
		print "runnning wget_file:",f
		os.system('bash '+f)
	except:
		print "error"
		continue

