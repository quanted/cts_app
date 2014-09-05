"""
Access to jchem web services.
"""

import requests
import json
import logging

baseUrl = 'http://pnnl.cloudapp.net/webservices' # This will soon change to a cgi server

headers = {'Content-Type' : 'application/json'}

formatConvertQuery = '/rest-v0/util/calculate/molExport' # See http://pnnl.cloudapp.net/webservices/apidocs#molExport
structQuery = '/rest-v0/data/sample/table/ChEBI_lite_3star/detail/' # (jchem) path for returning microspecies dist.
basicQuery = '/rest-v0/data/'
searchQuery = '/rest-v0/data/sample/table/ChEBI_lite_3star/search'


"""
Gets structure details such as pKa
postData - payload as dictionary 
"""
def getStructureDetails(postData):

	url = baseUrl + '/rest-v0/data/sample/table/ChEBI_lite_3star/detail/'

	data = json.dumps(postData)

	fileout = open('C:\\Users\\nickpope\\Desktop\\out.txt', 'w')
	fileout.write(data)

	response = requests.post(url, data=data, headers=headers)

	return response


