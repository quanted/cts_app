"""
Access to jchem web services
"""

import requests
import json
import logging

baseUrl = 'http://pnnl.cloudapp.net/webservices' # This will soon change to a local cgi server

headers = {'Content-Type' : 'application/json'}


Urls = {
	'exportUrl'	:	'/webservices/rest-v0/util/calculate/molExport',
	'utilUrl'	:	'webservices/rest-v0/util/detail',
}

# From REST.js in static/stylesheets/efs/js
 # Urls: {
 #    // jchem_kad urls
 #    insertUrl     : "/webservices/rest-v0/data/jchem_kad/table/kad/operation",
 #    detailUrl     : "/webservices/rest-v0/data/jchem_kad/table/kad/detail/",
 #    searchUrl     : "/webservices/rest-v0/data/jchem_kad/table/kad/search",
 #    imgUrl        : "/webservices/rest-v0/data/jchem_kad/table/kad/display/",

 #    // computed util urls
 #    exportUrl     : "/webservices/rest-v0/util/calculate/molExport",
 #    utilUrl       : "/webservices/rest-v0/util/detail",

 #    // EFS web services
 #    getMetabolitesUrl: "/efsws/rest/metabolizer",
 #    setMetabolitesUrl: "/efsws/rest/chemical/save-metabolites",
 #  },

"""
Gets details of molecule 
"""

def test_serverSide(text):
	return "success - server side"

def detailsBySmiles(mol):

	structures = [{ "structure" : mol }]
	include = ["structureData"]
	additionalFields = {
		"iupac" : "chemicalTerms(name)",
		"formula" :	"chemicalTerms(formula)",
		"mass" : "chemicalTerms(mass)",
		"smiles" : "chemicalTerms(molString('smiles'))"		 
	}
	parameters = { "structureData" : "mrv" }

	display = {"include":include, "additionalFields":additionalFields, "parameters":parameters}
	details = {"structures":structures, "display":display}

	data = json.dumps(details)

	url = baseUrl + '/rest-v0/util/detail/'

	response = requests.post(url, data=data, headers=headers)

	return response



def getStructureDetails(request, inputDict):

	url = ''

	if request == 'pka':

		url = baseUrl + '/rest-v0/data/sample/table/ChEBI_lite_3star/detail/'

	elif request == 'info':

		url = baseUrl + '/rest-v0/data/sample/table/ChEBI_lite_3star/detail/'

	data = json.dumps(inputDict)

	# fileout = open('C:\\Users\\nickpope\\Desktop\\out.txt', 'w')
	# fileout.write(data)

	response = requests.post(url, data=data, headers=headers)

	return response


