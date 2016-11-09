__author__ = 'np'

"""
CTS-oriented calls to jchem web services
"""

import requests
import json
import logging
from django.shortcuts import render
import datetime
import pytz
import os
from django.utils.safestring import mark_safe
from django.http import HttpResponse  # todo: remove this and only use requests


headers = { 'Content-Type': 'application/json' }


class Urls:
	cts_jchem_server = os.environ['CTS_JCHEM_SERVER']
	cts_efs_server = os.environ['CTS_EFS_SERVER']

	jchemBase = cts_jchem_server + '/webservices'

	# jchem ws urls:
	serverUrl = '/rest-v0'
	exportUrl = '/rest-v0/util/calculate/molExport'
	detailUrl = '/rest-v0/util/detail'
	hydroUrl = '/rest-v0/util/convert/hydrogenizer'
	standardizerUrl = '/rest-v0/util/convert/standardizer'

	# homegrown metabolizer ws:
	# efsBase = cts_efs_server + '/efsws/rest'
	efsBase = cts_efs_server + '/ctsws/rest'
	metabolizerUrl = efsBase + '/metabolizer'
	standardizerUrlEFS = efsBase + '/standardizer'


def getJchemVersion(request=None):
	"""
	Gets version of jchem being used.
	Initially intended for producing a log file.
	"""
	# NOTE: it's a GET
	url = Urls.jchemBase + Urls.serverUrl
	imgData = web_call(url, request, None)  # get response from jchem ws
	return imgData  # return dict of image data


def getChemDetails(request):
	"""
	getChemDetails

	Inputs:
	chem - chemical name (format: iupac, smiles, or formula)
	Returns:
	The iupac, formula, mass, and smiles string of the chemical
	along with the mrv of the chemical (to display in marvinjs)
	"""

	addH = False

	try:
		chem = request.data.get('chemical')
		logging.info("> using DATA <")
	except AttributeError:
		logging.info("> using POST <")
		chem = request.POST.get('chemical')
		if 'addH' in request.POST:
			logging.info("> adding explicitH")
			addH = True
	else:
		if 'addH' in request.data:
			logging.info("> adding explicitH")
			addH = True
	finally:
		ds = DataStructures()
		data = ds.chemDeatsStruct(chem, addH)  # format request to jchem
		data = json.dumps(data)  # convert dict to json string
		url = Urls.jchemBase + Urls.detailUrl
		return web_call(url, request, data)


def smilesToImage(request):
	"""
	smilesToImage

	Returns image (.png) url for a 
	given SMILES
	"""
	smiles = request.POST.get('smiles')
	imgScale = request.POST.get('scale')
	imgWidth = request.POST.get('width')
	imgHeight = request.POST.get('height')
	imgType = request.POST.get('type')

	img_type = request.POST.get('type')

	# NOTE: Requesting image without width or height but scale
	# returns an image that just fits the molecule with nice resoltuion.
	# Providing width and height without scale might return a higher
	# resolution image for metabolites!
	
	request = {
		"structures": [
			{"structure": smiles}
		],
		"display": {
			"include": ["image"],
			"parameters": {
				"image": {
				}
			}
		}
	}

	if imgType:
		request['display']['parameters']['image'].update({'type': imgType})
	else:
		request['display']['parameters']['image'].update({'type': 'png'})

	if imgHeight:
		# these are metabolites in the space tree:
		request['display']['parameters']['image'].update({"width": imgWidth, "height": imgHeight})
	else:
		request['display']['parameters']['image'].update({'width': imgWidth, 'scale': imgScale})
	# 	# these are the popup image ones (large):
	# 	request['display']['parameters']['image'].update({'scale': imgScale})  # trying just a scale no width (may need width)

	data = json.dumps(request)  # to json string
	url = Urls.jchemBase + Urls.detailUrl
	imgData = web_call(url, request, data)  # get response from jchem ws
	return imgData  # return dict of image data


def convertToSMILES(request):
	"""
	convertToSMILES

	Inputs: chemical as mrv, smiles, etc. (chemaxon recognized)
	Returns: SMILES string of chemical
	"""
	chemStruct = request.data.get('chemical')  # chemical in <cml> format (marvin sketch)
	request = {
		"structure": chemStruct,
		# "inputFormat": "mrv",
		"parameters": "smiles"
	}
	data = json.dumps(request)  # serialize to json-formatted str
	url = Urls.jchemBase + Urls.exportUrl
	smilesData = web_call(url, request, data)  # get responset))
	return smilesData


def getChemSpecData(request):
	"""
	getChemSpecData

	Gets pKa values and microspecies distribution
	for a given chemical

	Inputs - data types to get (e.g., pka, tautomer, etc.),
	and all the fields from the 3 tables.
	"""
	ds = DataStructures()
	addH = False
	if 'addH' in request.data:
		addH = True
	data = ds.chemSpecStruct(request.data, addH)  # format request to jchem
	data = json.dumps(data)
	url = Urls.jchemBase + Urls.detailUrl
	results = web_call(url, request, data)
	return results


def getTransProducts(request):
	"""
	Makes request to metabolizer
	"""
	url = Urls.metabolizerUrl
	data = json.dumps(request.POST)
	results = web_call(url, request, data)
	return results


# def getpchemprops(request):
#     """
# 	Calls pchemprop model to get pchem props 
# 	for a given molecule. This ws was
# 	originally meant for getting pchem props 
# 	for METABOLITES on the gentrans output page.

# 	This is only here for accessing pchemprop_model
# 	via frontend ajax calls
# 	"""
#     from models.pchemprop import pchemprop_output
#     pchemprop_obj = pchemprop_output.pchempropOutputPage(request, True)  # run model for metabolite
#     return json.dumps(pchemprop_obj.checkedCalcsAndPropsDict)


def getStructInfo(structure):
	"""
	Appends structure info to image url
	Input: structure in .mrv format
	Output: dict with structure's info (i.e., formula, iupac, mass, smiles),
	or dict with aforementioned keys but None values
	"""
	request = requests.Request(data={"chemical": structure, "addH": True})
	response = getChemDetails(request)
	structDict = json.loads(response.content)
	infoDictKeys = ['formula', 'iupac', 'mass', 'smiles','exactMass']
	infoDict = {key: None for key in infoDictKeys}  # init dict with infoDictKeys and None vals
	struct_root = {}  # root of data in structInfo
	if 'data' in structDict:
		struct_root = structDict['data'][0]
		infoDict.update({"formula": struct_root['formula']})
		infoDict.update({"iupac": struct_root['iupac']})
		infoDict.update({"mass": struct_root['mass']})
		infoDict.update({"smiles": struct_root['smiles']})
		infoDict.update({'exactMass': struct_root['exactMass']})
	return infoDict


def removeExplicitHFromSMILES(request):
	"""
	removes explicit hydrogens from SMILES string.
	expects request to have 'smiles' key
	"""
	try:
		smiles = request.data.get('smiles')
	except Exception as e:
		logging.info("Exception at removeExplicitHFromSMILES: {}".format(e))
		return
	else:
		post_data = {
			"structure": smiles,
			"parameters": "smiles",
			"filterChain": [
				{
					"filter": "hydrogenizer",
					"parameters": {
						"method": "DEHYDROGENIZE"
					}
				}
			]
		}
		url = Urls.jchemBase + Urls.exportUrl
		results = web_call(url, request, json.dumps(post_data))
		return results


def getMass(request):
	"""
	get mass of structure from jchem ws
	"""
	try:
		smiles = request.data.get('smiles')
	except Exception as e:
		logging.info("Exception retrieving mass from jchem: {}".format(e))
		raise
	post_data = {
		"structures": [
			{"structure": smiles}
		],
		"display": {
			"include": [
				"structureData"
			],
			"additionalFields": {
				"mass": "chemicalTerms(mass)"
			},
			"parameters": {
				"structureData": "smiles"
			}
		}
	}
	url = Urls.jchemBase + Urls.detailUrl
	results = web_call(url, request, json.dumps(post_data))
	return results


def singleFilter(request):
	"""
	Calls single EFS Standardizer filter
	for filtering SMILES
	"""
	try:
		smiles = request.data.get('smiles')
		action = request.data.get('action')
	except Exception as e:
		logging.info("Exception retrieving mass from jchem: {}".format(e))
		raise
	post_data = {
		"structure": smiles,
		"actions": [
			action
		]
	}
	url = Urls.standardizerUrlEFS
	results = web_call(url, request, json.dumps(post_data))
	return results


def clearStereo(request):
	"""
	clear stereoisomers from structure
	"""
	try:
		smiles = request.data.get('smiles')
	except Exception as e:
		logging.info("Exception retrieving mass from jchem: {}".format(e))
		raise
	post_data = {
		"structure": smiles,
		"actions": [
			"clearStereo"
		]
	}
	url = Urls.standardizerUrlEFS
	results = web_call(url, request, json.dumps(post_data))
	return results


def transform(request):
	"""
	transform N(=O)=O >> [N+](=O)[O-]
	"""
	try:
		smiles = request.data.get('smiles')
	except Exception as e:
		logging.info("Exception retrieving mass from jchem: {}".format(e))
		raise
	post_data = {
		"structure": smiles,
		"actions": [
			"transform"
		]
	}
	url = Urls.standardizerUrlEFS
	results = web_call(url, request, json.dumps(post_data))
	return results


def filterSMILES(request):
	"""
	cts ws call to jchem to perform various
	smiles processing before being sent to
	p-chem calculators
	"""
	try:
		smiles = request.data.get('smiles')
	except Exception as e:
		logging.info("exception at transformSMILES: {}".format(e))
		return
	else:
		# POST data for efs standardizer ws:
		post_data = {
			"structure": smiles,
			"actions": [
				"removeExplicitH",
				"transform",
				"tautomerize",
				"neutralize"
			]
		}
		url = Urls.standardizerUrlEFS # http://server/efsws/rest/standardizer
		results = web_call(url, request, json.dumps(post_data))
		return results


def web_call(url, request, data):
	"""
	Makes the request to a specified URL
	and POST data. Returns an http response.
	"""
	try:
		if data == None:
			response = requests.get(url, timeout=10)
		else:
			response = requests.post(url, data=data, headers=headers, timeout=30)
		return response
	except requests.exceptions.RequestException as e:
		logging.warning("error at web call: {} /error".format(e))
		raise e



class DataStructures:
	def chemDeatsStruct(self, chemical, addH=False):
		# return json data for chemical details
		chemDeatsDict = {
			"structures": [
				{"structure": chemical}
			],
			"display": {
				"include": [
					"structureData"
				],
				"additionalFields": {
					"formula": "chemicalTerms(formula)",
					"iupac": "chemicalTerms(name)",
					"mass": "chemicalTerms(mass)",
					"exactMass": "chemicalTerms(exactMass)",
					"smiles": "chemicalTerms(molString('smiles'))",
				},
				"parameters": {
					"structureData": "mrv"
				}
			}
		}
		# if addH:
			# chemDeatsDict = addExplicitH(chemDeatsDict)
			# chemDeatsDict = removeExplicitH(chemDeatsDict)
		return chemDeatsDict


	def chemSpecStruct(self, dic, addH=False):

		# don't forget about pKa_decimal

		keys = ["isoelectricPoint", "pKa", "majorMicrospecies", "stereoisomer",
				"tautomerization", "logP", "logD", "solubility"]

		structures = []
		if 'chemical' in dic:
			structures = [{"structure": dic["chemical"]}]

		includeList = []
		paramsDict = {}  # dict of dict where latter dict has key of param and vals of param vals

		for key, value in dic.items():
			if key in keys:
				includeList.append(key)  # add parameter to "include" list
				paramsDict.update({key: value})

		display = {"include": includeList, "parameters": paramsDict}
		dataDict = {"structures": structures, "display": display}

		if addH:
			dataDict = addExplicitH(dataDict)

		return dataDict


def addExplicitH(dataDict):
	"""
	Add explicitH option to data dictionary
	for jchem web call. Assumes 'display' key
	exists.
	"""
	filterChain = [{
					   "filter": "hydrogenizer",
					   "parameters": {"method": "HYDROGENIZE"}
				   }]
	dataDict['display'].update({'filterChain': filterChain})
	return dataDict


def removeExplicitH(dataDict):
	"""
	Add explicitH option to data dictionary
	for jchem web call. Assumes 'display' key
	exists.
	"""
	filterChain = [{
					   "filter": "hydrogenizer",
					   "parameters": {"method": "DEHYDROGENIZE"}
				   }]
	dataDict['display'].update({'filterChain': filterChain})
	return dataDict


def gen_jid():
	ts = datetime.datetime.now(pytz.UTC)
	localDatetime = ts.astimezone(pytz.timezone('US/Eastern'))
	jid = localDatetime.strftime('%Y%m%d%H%M%S%f')
	return jid