#!/usr/bin/env python

"""Usage: eagleianalytics.py <csv> <outfile>

Process csv file from Google Analytics and lookup eagle-i resource

Arguments:
	csv    	required csv file
	outfile	csv file with resource information added

"""

import requests, codecs, csv, docopt
from bs4 import BeautifulSoup

# lookup some info for an eagle-i uri
def landingPage(uri):
	url = 'http://eagle-i.itmat.upenn.edu' + uri + '?forceXML'
	payload = {'uri': url}
	uriInfo = ()

	r = requests.get(url)
	# outfile = codecs.open('./out_.xml','w','utf-8') # for inspecting xml
	# outfile.write(r.text)
	soup = BeautifulSoup(r.text, "lxml")
	assertedType = soup.find("asserted-types")
	inferredTypes = soup.find("inferredTypes")
	
	try:
		resourceName = soup.resource.string
	except:
		resourceName = "BAD LANDING PAGE LINK"

	try:
		resourceType = assertedType.resource.string
	except:
		resourceType = "NO RESOURCE TYPE INFO"

	# if uri corresponds to resource find owning organization
	if(soup.find(uri="http://xmlns.com/foaf/0.1/Organization") or soup.find(uri="http://xmlns.com/foaf/0.1/Person")):
		pass
	# used by case (should find the used by or located in instead of going resource by resource)
	# software, database, or protocol
	elif(soup.find(uri="http://purl.obolibrary.org/obo/ERO_0000071") or \
		 soup.find(uri="http://purl.obolibrary.org/obo/ERO_0001716") or \
		 soup.find(uri="http://purl.obolibrary.org/obo/OBI_0000272")):
		loc = soup.find(uri="http://purl.obolibrary.org/obo/ERO_0000070")
	# service
	elif(soup.find(uri="http://purl.obolibrary.org/obo/ERO_0000005")):
		loc = soup.find(uri="http://purl.obolibrary.org/obo/ERO_0000390")
	# non-software resources
	else:
		loc = soup.find(uri="http://purl.obolibrary.org/obo/RO_0001025")

	try:
		locP = loc.parent.parent
		locatedIn = locP.object.resource.string
	except:
		locatedIn = "N/A"

	uriInfo = (resourceName, resourceType, locatedIn)
	return (resourceName, resourceType, locatedIn)

if __name__ == '__main__':
	arguments = docopt.docopt(__doc__)
	fieldnames = ['Service Provider', 'City', 'Landing Page', 'Full Referrer', \
				  'Date', 'Users', 'Organic Searches', 'Resource Name', \
				  'Resource Type', 'Resource Location']
	
	with open(arguments['<csv>'], 'rb') as csvfile:
		info = list()
		for i in range(0,7):  # skip header rows
			next(csvfile)
		reader = csv.DictReader(csvfile, fieldnames=fieldnames, restval='')
		for row in reader:
			if(row['Landing Page'] == '/'):
				pass
			elif(row['Landing Page'] == '(not set)'):
				pass
			elif(row['Landing Page'] == ''):
				pass
			else:
				rowUriInfo = landingPage(row['Landing Page'])
				row['Resource Name'] = rowUriInfo[0]
				row['Resource Type'] = rowUriInfo[1]
				row['Resource Location'] = rowUriInfo[2]
				#print "\t".join(rowUriInfo)
			info.append(row)
	
	# comma separated (alone) for output problematic because some fields
	# contain commas
	with open(arguments['<outfile>'], 'w') as csvoutfile:
		csvoutfile.write("\t".join(fieldnames))
		csvoutfile.write("\n")
		#writer.writerows(info)
		for row in info:
			tmp = list()
			for i in fieldnames:
				tmp.append(row[i])
			csvoutfile.write(("\t".join(tmp)).encode('utf-8'))
			csvoutfile.write("\n")