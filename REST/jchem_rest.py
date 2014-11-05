"""
Access to jchem web services
(np)
"""

import requests
import json
import logging
import views.misc
from django.http import HttpResponse
from django.http import HttpRequest
from xml.sax.saxutils import escape
import datetime
import pytz


headers = {'Content-Type' : 'application/json'}


class Urls:

	base = 'http://pnnl.cloudapp.net/webservices' # old ws location 
	base2 = 'http://pnnl.cloudapp.net/efsws' # metabolizer base
	# base = 'http://134.67.114.2/webservices'
	# base = 'http://134.67.114.2/efsws/rest' # antiquated, but functioning, WS

	# jchem ws urls:
	exportUrl = '/rest-v0/util/calculate/molExport'
	detailUrl = '/rest-v0/util/detail'

	metabolizerUrl = '/rest/metabolizer'


class CTS_To_Jchem:

	pkaKeys = ["pKa_decimals", "pKa_pH_lower","pKa_pH_upper", "pKa_pH_increment"]
	majorMicroKeys = ["pH_microspecies"]
	isoPtKeys = ["isoelectricPoint_pH_increment"]

	tautKeys = ["tautomer_maxNoOfStructures", "tautomer_pH"]
	stereoKeys = ["stereoisomers_maxNoOfStructures"]	


"""
API Documentation Page
"""
def doc(request):
	text_file2 = open('REST/doc_text.txt','r')

	xx = text_file2.read()

	response = HttpResponse()
	response.write(xx)

	return response



"""
getChemDeats

Inputs:
chem - chemical name (format: iupac, smiles, or formula)
Returns:
The iupac, formula, mass, and smiles string of the chemical
along with the mrv of the chemical (to display in marvinjs)
"""
def getChemDeats(request):
	queryDict = request.POST
	chem = queryDict.get('chemical') # chemical name
	ds = data_structures()
	data = ds.getChemDeats(chem) # format request to jchem
	url = Urls.base + Urls.detailUrl
	return web_call(url, request, data)


"""
smilesToImage

Returns image (.png) url for a 
given SMILES
"""
def smilesToImage(request):
	smiles = request.POST.get('smiles')
	imageWidth = request.POST.get('width')
	imageHeight = request.POST.get('height')
	request = {
		"structures": [
			{"structure": smiles}
		],
		"display": {
			"include": ["image"],
			"parameters": {
				"image": {
					"width": imageWidth,
					"height": imageHeight
				}
			}
		}
	}
	data = json.dumps(request) # to json string
	url = Urls.base + Urls.detailUrl
	imgData = web_call(url, request, data) # get response from jchem ws
	return imgData # return dict of image data


"""
mrvToSmiles

Gets SMILES string for chemical drawn
in Marvin Sketch
"""
def mrvToSmiles(request):
	queryDict = request.POST
	chemStruct = queryDict.get('chemical') # chemical in <cml> format (marvin sketch)
	request = {
		"structure" : chemStruct,
		"inputFormat" : "mrv",
		"parameters" : "smiles"
	}
	data = json.dumps(request) # serialize to json-formatted str
	url = Urls.base + Urls.exportUrl
	smilesData = web_call(url, request, data) # get responset))
	data = json.loads(smilesData.content)
	request = HttpRequest()
	request.POST = { "chemical": data['structure'] }
	return getChemDeats(request) # return smiles along with other info


"""
getChemSpecData

Gets pKa values and microspecies distribution
for a given chemical

Inputs - data types to get (e.g., pka, tautomer, etc.),
and all the fields from the 3 tables.
"""
def getChemSpecData(request):
	ds = data_structures()
	data = ds.chemSpecStruct(request.POST) # format request to jchem
	data = json.dumps(data)
	url = Urls.base + Urls.detailUrl
	results = web_call(url, request, data)
	return results


"""
Makes request to metabolizer on pnnl server
"""
def getTransProducts(request):
	url = Urls.base2 + Urls.metabolizerUrl
	data = json.dumps(request.POST)
	results = web_call(url, request, data)
	return results


"""
Makes the request to a specified URL
and POST data. Returns an http response.
"""
def web_call(url, request, data):
	callback_response = HttpResponse()
	message = '\n' + "URL: " + '\n' + url + '\n\n'
	message = message + "POST Data: " + '\n' + str(data) + '\n\n'
	try:
		logging.warning("trying to get response...")
		response = requests.post(url, data=data, headers=headers, timeout=60)
		logging.warning("success.")
		message = message + "Response: " + '\n' + response.content + '\n\n'
		callback_response.write(response.content)
		return callback_response
	except:
		logging.warning("Error in web call")
		callback_response.write(message)
		return callback_response


class data_structures:

	def getChemDeats(self, chemical):
		# return json data for chemical details
		return """{"structures": [{"structure": """ + '"'  + chemical + '"' + """}], "display": {"include": ["structureData"], "additionalFields": {"formula": "chemicalTerms(formula)", "iupac": "chemicalTerms(name)", "mass": "chemicalTerms(mass)", "smiles": "chemicalTerms(molString('smiles'))"}, "parameters": {"structureData": "mrv"}}}"""
		
	def chemSpecStruct(self, dic):
		# don't forget about pKa_decimal
		pkaKeys = ["pKa_pH_lower","pKa_pH_upper", "pKa_pH_increment"]
		majorMicroKeys = ["pH_microspecies"]
		isoPtKeys = ["isoelectricPoint_pH_increment"]

		tautKeys = ["tautomer_maxNoOfStructures", "tautomer_pH"]
		stereoKeys = ["stereoisomers_maxNoOfStructures"]

		structures = []
		if 'chem_struct' in dic:
			structures = [ { "structure": dic["chem_struct"] } ]

		pkaDict, majorMicroDict, isoPtDict = {}, {}, {}  
		tautDict, stereoDict = {}, {}

		for key in dic.keys():
			if key in pkaKeys:
				pkaDict.update({key: dic[key]})
			if key in majorMicroKeys:
				majorMicroDict.update({key: dic[key]})
			if key in isoPtKeys:
				isoPtDict.update({key: dic[key]})
			if key in tautKeys:
				tautDict.update({key: dic[key]})
			if key in stereoKeys:
				stereoDict.update({key: dic[key]})

		paramsDict, inlcudeList = {}, []
		if pkaDict:
			paramsDict["pKa"] = pkaDict
			paramsDict["majorMicrospecies"] = majorMicroDict
			paramsDict["isoelectricPoint"] = isoPtDict
			inlcudeList.append("pKa")
			inlcudeList.append("majorMicrospecies")
			inlcudeList.append("isoelectricPoint")
		if tautDict:
			paramsDict["tautomerization"] = tautDict
			inlcudeList.append("tautomerization")
		if stereoDict:
			paramsDict["stereoisomer"] = stereoDict
			inlcudeList.append("stereoisomer")

		display = {"include": inlcudeList, "parameters": paramsDict}

		dataDict = {"structures": structures, "display": display}

		return dataDict


def gen_jid():
    ts = datetime.datetime.now(pytz.UTC)
    localDatetime = ts.astimezone(pytz.timezone('US/Eastern'))
    jid = localDatetime.strftime('%Y%m%d%H%M%S%f')
    return jid



	