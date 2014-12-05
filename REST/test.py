from django.http import HttpResponse
import logging
import json
import requests



baseUrl = 'http://pnnl.cloudapp.net/webservices' # This will soon change to a local cgi server
headers = {'Content-Type' : 'application/json'}

def testPage(request, chem):

	structures = [{ "structure" : chem }]
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

	chemDetails = requests.post(url, data=data, headers=headers)

	# fileout = open('C:\\Users\\nickpope\\Desktop\\out.txt', 'w')
	# fileout.write(data)
	# fileout.close()

	# return response
	response = HttpResponse()
	response.write(chemDetails.content)

	logging.warning(response)

	return response