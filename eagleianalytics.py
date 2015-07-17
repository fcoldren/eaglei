#!/usr/bin/env python

"""Usage: eagleianalytics.py <csv>

Process csv file from Google Analytics and lookup eagle-i resource

Arguments:
	csv    required csv file

"""

import requests, codecs, csv, docopt
from bs4 import BeautifulSoup

# lookup some info for an eagle-i uri
def landingPage(uri):
	url = 'http://eagle-i.itmat.upenn.edu' + uri + '?forceXML'
	payload = {'uri': url}

	r = requests.get(url)
	#outfile = codecs.open('./out_t7.xml','w','utf-8') # for inspecting xml
	#outfile.write(r.text)
	soup = BeautifulSoup(r.text, "lxml")
	assertedType = soup.find("asserted-types")
	inferredTypes = soup.find("inferredTypes")

	resourceName = soup.resource.string
	resourceType = assertedType.resource.string

	# if uri corresponds to resource find owning organization
	if(soup.find(uri="http://xmlns.com/foaf/0.1/Organization") or soup.find(uri="http://xmlns.com/foaf/0.1/Person")):
		pass
	else:
		loc = soup.find(uri="http://purl.obolibrary.org/obo/RO_0001025")
		locP = loc.parent.parent
		locatedIn = locP.object.resource.string

	print resourceName, resourceType,
	try:
		print locatedIn
	except:
		print "N/A"

if __name__ == '__main__':
	arguments = docopt.docopt(__doc__)
	fieldnames = ['Service Provider', 'City', 'Landing Page', 'Full Referrer', \
				  'Country', 'Users', 'Organic Searches']
	with open(arguments['<csv>'], 'rb') as csvfile:
		# skip header rows
		for i in range(0,7):
			next(csvfile)
		reader = csv.DictReader(csvfile, fieldnames=fieldnames)
		print("Adding row numbers...")
		for row in reader:
			print(row['Landing Page'], row['City'])

# t1 = '/i/00000138-7cbe-8ce9-fbab-3b8480000000' # core lab example
# t2 = '/i/00000141-eb21-a19f-91c7-0c6080000000' # person example
# t4 = '/i/00000142-38e7-afa1-91c7-0c6080000000'
# t5 = '/i/00000138-7c75-c358-fbab-3b8480000000' # department
# t6 = '/i/0000013c-d9d6-4f98-f162-a2b280000000' # laboratory
# t7 = '/i/0000013a-c1be-84b1-d69a-d90d80000000'




# landingPage(t1)
# landingPage(t2)
# landingPage(t7)

#print infile