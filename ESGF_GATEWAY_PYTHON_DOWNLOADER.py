import os, sys, re, glob, urllib2
# http://esg-datanode.jpl.nasa.gov/esg-search/wget
# http://esg-datanode.jpl.nasa.gov/esg-search/wget?offset=300&limit=100
# http://pcmdi9.llnl.gov/esg-search/wget?cf_standard_name=air_temperature&experiment=decadal2000&project=CMIP5
# http://pcmdi9.llnl.gov/esg-search/wget?cf_standard_name=air_temperature&experiment=decadal2000&project=CMIP5

# variable names
experiments = ["historical","rcp26","rcp45","rcp60","rcp85"]
time_frequencies = ["mon"] 
realms = ["atmos"] 
CMOR_tables = ["Amon"] 
ensembles = ["r1i1p1"] 
cf_standard_names = ["tas","tasmin","tasmax","pr","psl","uas","vas","sfcWind","tauu","tauv","ua","va","hur","hurs","hus","huss","rsds","clt","sit","sic"]

# this is the name or the list of names that the search will query on.  I am beginning with this one.
base_url="http://pcmdi9.llnl.gov/esg-search/wget?"

response = urllib2.urlopen(base_url)

# loop through all of the aspects of the naming convention for each var
for experiment in experiments:
	for time_frequency in time_frequencies:
		for realm in realms:
			for CMOR_table in CMOR_tables:
				for ensemble in ensembles:
					for cf_standard_name in cf_standard_names:
						# here we create the new url name to generate the wget script needed to harvest the data
						new_url=base_url+"experiment="+experiment+"&"+"time_frequency="+time_frequency+"&"+"realm="+realm+"&"+"cmor_table="+CMOR_table+"&"+"ensemble="+ensemble+"&"+"variable="+cf_standard_name+"&"+"project=CMIP5"

						response = urllib2.urlopen(new_url)
						
						print "downloading " + new_url

						try:
							# Open our local file for writing
							local_file = open("/Users/snap/wget.sh", "wt")
							#Write to our local file
							local_file.write(response.read())
							local_file.close()

							# this line will initiate the script and it should bring up a java applet for login.
							os.system('bash /Users/snap/test.sh')

						except:
							continue



