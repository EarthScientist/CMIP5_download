# Basically, can we run the command one-by-one using the stuff before and after ".nc"
# 	this is where we read in the wget file produced because I have not figured out how to 
#	pass the response.read() over for testing...  may change in the future...
# lets bring back in the wget file produced by the PCMDI9 server
wget_file=open(os.path.join(outPath,model+'_'+variable+'_'+experiment+"_"+time_frequency+"_"+realm+'_'+CMOR_table+'_'+ensemble+'.sh'),'r')
# here we reach the lines from the file
lines=wget_file.readlines()

# the url to examine
new_url=base_url+"model="+model+"&"+"experiment="+experiment+"&"+"time_frequency="+time_frequency+"&"+"realm="+realm+"&"+"cmor_table="+CMOR_table+"&"+"ensemble="+ensemble+"&"+"variable="+variable+"&"+"project=CMIP5"+"&"+"latest=true"

# the response from the url
response = urllib2.urlopen(new_url)

# the response line is:
lines=response.readlines()

#create an empty list object
lineList=[]

# lOOP THORUGH THE LIST: (where i is line_number)
for i, line in enumerate(lines):
	pattern = re.compile(".nc'") # looking for the lines with the .nc' in the line.  this will indicate the ones we want
	if pattern.search(line):
		print i, lines[i]
		lineList.append(i)

beginLine=min(lineList)
endLine=max(lineList)

wget_new_part1 = lines[0:beginLine]
wget_new_part2 = lines[endLine+1:i]

for l in lineList:
	new_wget_file=open(,'wt')
	lineList[l]



with io.open("test",'w') as file: