__author__ = 'np'

"""
CTS-oriented calls to jchem web services
"""

import requests
import json
import logging
import os


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

	# CTSWS (formerlly EFS) metabolizer endpoints:
	efsBase = cts_efs_server + '/ctsws/rest'
	metabolizerUrl = efsBase + '/metabolizer'
	standardizerUrlEFS = efsBase + '/standardizer'


def getChemDetails(request_obj):
	"""
	getChemDetails

	Inputs:
	chem - chemical name (format: iupac, smiles, or formula)
	Returns:
	The iupac, formula, mass, and smiles string of the chemical
	along with the mrv of the chemical (to display in marvinjs)
	"""
	chemical = request_obj.get('chemical')

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

	url = Urls.jchemBase + Urls.detailUrl
	return web_call_new(url, chemDeatsDict)


def smilesToImage(request_obj):
	"""
	smilesToImage

	Returns image (.png) url for a 
	given SMILES
	"""
	smiles = request_obj.get('smiles')
	imgScale = request_obj.get('scale')
	imgWidth = request_obj.get('width')
	imgHeight = request_obj.get('height')
	imgType = request_obj.get('type')

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

	url = Urls.jchemBase + Urls.detailUrl
	imgData = web_call_new(url, request)  # get response from jchem ws
	return imgData  # return dict of image data


def convertToSMILES(request_obj):
	"""
	convertToSMILES

	Inputs: chemical as mrv, smiles, etc. (chemaxon recognized)
	Returns: SMILES string of chemical
	"""
	chemStruct = request_obj.get('chemical')  # chemical in <cml> format (marvin sketch)
	data = {
		"structure": chemStruct,
		# "inputFormat": "mrv",
		"parameters": "smiles"
	}
	url = Urls.jchemBase + Urls.exportUrl
	return web_call_new(url, data)  # get responset))


def getTransProducts(request_obj):
	"""
	Makes request to metabolizer
	"""
	url = Urls.metabolizerUrl
	return web_call_new(url, request_obj)


def getStructInfo(structure):
	"""
	Appends structure info to image url
	Input: structure in .mrv format
	Output: dict with structure's info (i.e., formula, iupac, mass, smiles),
	or dict with aforementioned keys but None values
	"""
	structDict = getChemDetails({"chemical": structure, "addH": True})
	infoDictKeys = ['formula', 'iupac', 'mass', 'smiles','exactMass']
	infoDict = {key: None for key in infoDictKeys}  # init dict with infoDictKeys and None vals
	struct_root = {}  # root of data in structInfo
	if 'data' in structDict:
		struct_root = structDict['data'][0]
		infoDict.update({
			"formula": struct_root['formula'],
			"iupac": struct_root['iupac'],
			"mass": struct_root['mass'],
			"smiles": struct_root['smiles'],
			'exactMass': struct_root['exactMass']
		})
	return infoDict


def getMass(request_obj):
	"""
	get mass of structure from jchem ws
	"""
	chemical = request_obj.get('chemical')
	logging.info("jchem_rest getting mass for {}".format(chemical))
	post_data = {
		"structures": [
			{"structure": chemical}
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
	return web_call_new(url, post_data)


def singleFilter(request_obj):
	"""
	Calls single EFS Standardizer filter
	for filtering SMILES
	"""
	try:
		smiles = request_obj.get('smiles')
		action = request_obj.get('action')
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
	return web_call_new(url, post_data)


def filterSMILES(request_obj):
	"""
	cts ws call to jchem to perform various
	smiles processing before being sent to
	p-chem calculators
	"""
	smiles = request_obj.get('smiles')

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
	return web_call_new(url, post_data)


def web_call_new(url, data):
	"""
	Makes the request to a specified URL
	and POST data. Returns resonse data as dict
	"""

	# TODO: Deal with errors more granularly... 403, 500, etc.
	try:
		if data == None:
			response = requests.get(url, timeout=10)
		else:
			response = requests.post(url, data=json.dumps(data), headers=headers, timeout=30)
		return json.loads(response.content)
	except requests.exceptions.RequestException as e:
		logging.warning("error at web call: {} /error".format(e))
		raise e