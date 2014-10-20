"""
Access to jchem web services
"""

import requests
import json
import logging
import views.misc
from django.http import HttpResponse



headers = {'Content-Type' : 'application/json'}


# Urls = {
# 	'exportUrl'	:	'/webservices/rest-v0/util/calculate/molExport',
# 	'utilUrl'	:	'/rest-v0/util/detail',
# }

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

class Urls:

	# base = 'http://pnnl.cloudapp.net/webservices' # Old WS location 
	base = 'http://134.67.114.2/webservices'

	exportUrl = '/rest-v0/util/calculate/molExport'
	utilUrl = '/rest-v0/util/detail'



"""
API Documentation Page
"""
def doc(request):
	text_file2 = open('REST/doc_text.txt','r')

	xx = text_file2.read()

	# html = xx

	response = HttpResponse()
	response.write(xx)

	return response



"""
detailsBySmiles

Inputs:
chem - chemical name (format: iupac, smiles, or formula)
Returns:
The iupac, formula, mass, and smiles string of the chemical
along with the mrv of the chemical (to display in marvinjs)
"""
def detailsBySmiles(request):

	queryDict = request.POST

	logging.warning("inside jchem_rest - detailsBySmiles")

	# logging.warning(queryDict)

	chem = queryDict.get('chemical')

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

	# logging.warning(data)

	url = Urls.base + Urls.utilUrl

	callback_response = HttpResponse()

	try:
		response = requests.post(url, data=data, headers=headers)

		message = '\n' + "URL: " + '\n' + url + '\n\n'
		message = message + "POST Data: " + '\n' + data + '\n\n'
		message = message + "Response: " + '\n' + response.content + '\n\n'

		logging.warning(message)

		callback_response.write(response.content)

		return callback_response

	except:
		response = views.misc.requestTimeout(request)
		logging.warning("ERROR, content: " + response.content)
		callback_response.write(response.content)

		return callback_response



"""
mrvToSmiles

Gets SMILES string for chemical drawn
in Marvin Sketch
"""
def mrvToSmiles(request):

	queryDict = request.POST

	# logging.warning(queryDict)

	chemStruct = queryDict.get('chemical') # chemical in <cml> format (marvin sketch)

	request = {
		"structure" : chemStruct,
		"inputFormat" : "mrv",
		"parameters" : "smiles"
	}

	data = json.dumps(request)

	url = Urls.base + Urls.exportUrl

	logging.warning("inside jchem_rest - mrvToSmiles")

	callback_response = HttpResponse()

	try:
		response = requests.post(url, data=data, headers=headers)
		# logging.warning("chemical: " + chem)
		# logging.warning("SUCCESS, content: " + response.content)

		message = '\n' + "URL: " + '\n' + url + '\n\n'
		message = message + "POST Data: " + '\n' + data + '\n\n'
		message = message + "Response: " + '\n' + response.content + '\n\n'

		logging.warning(message)

		callback_response.write(response.content)

		return callback_response

	except:
		response = views.misc.requestTimeout(request)
		logging.warning("ERROR, content: " + response.content)
		callback_response.write(response.content)

		return callback_response




	