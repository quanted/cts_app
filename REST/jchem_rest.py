"""
Access to jchem web services
(np)
"""

import requests
import json
import logging
from django.template import Template, Context
from django.shortcuts import render
import datetime
import pytz
import os
import time

from django.http import HttpResponse # todo: remove this and only use requests


headers = {'Content-Type' : 'application/json'}


class Urls:

	cts_jchem_server = os.environ['CTS_JCHEM_SERVER']
	jchemBase = cts_jchem_server + '/webservices'

	# jchem ws urls:
	exportUrl = '/rest-v0/util/calculate/molExport'
	detailUrl = '/rest-v0/util/detail'
	hydroUrl = '/rest-v0/util/convert/hydrogenizer'
	standardizerUrl = '/rest-v0/util/convert/standardizer'

	# homegrown metabolizer ws:
	efsBase = cts_jchem_server + '/efsws/rest'
	metabolizerUrl = efsBase + '/metabolizer'


class JchemProperty(object):
	def __init__(self):
		self.propsList = ['pKa', 'isoelectricPoint', 'majorMicrospecies', 'tautomerization', 'stereoisomer']
		self.baseUrl = os.environ['CTS_JCHEM_SERVER']
		self.name = ''
		self.url = ''
		self.structure = '' # cas, smiles, iupac, etc. 
		self.postData = {},
		self.results = {}

	def setPostDataValue(self, propKey, propValue):
		"""
		Can set one key:value with (propKey, propValue)
		"""
		try:
			self.postData[self.name][propKey] = propValue
		except KeyError:
			logging.warning("key {} does not exist".format(propKey))
			return None
		except Exception as e:
			logging.warning("error occured: {}".format(e))
			return None
	
	def setPostDataValues(self, multiKeyValueDict):
		"""
		Can set multiple key:values at once
		"""
		try:
			for key, value in multiKeyValueDict.items():
				self.postData[self.name][key] = value
		except KeyError:
			logging.warning("key {} does not exist".format(key))
			return None
		except Exception as e:
			logging.warning("error occured: {}".format(e)) 	
			return None

	def makeDataRequest(self, structure): 
		url = self.baseUrl + self.url
		self.postData.update({
			"result-display": {
	            "include":["structureData", "image"],
	            "parameters":{
	                "structureData":"smiles"
	            }
        	}
        })
		postData = {
			"structure": structure,
			"parameters": self.postData
		}
		try:
			response = requests.post(url, data=json.dumps(postData), headers=headers, timeout=60)
		except requests.exceptions.ConnectionError as ce:
			logging.warning("connection exception: {}".format(ce))
			return None
		except requests.exceptions.Timeout as te:
			logging.warning("timeout exception: {}".format(te))
			return None
		else:
			self.results = json.loads(response.content)
			return response

	@classmethod
	def getPropObj(self, prop):
		"""
		For getting prop objects in a general,
		loop-friendly way
		"""
		if prop == 'pKa':
			return Pka()
		elif prop == 'isoelectricPoint':
			return IsoelectricPoint()
		elif prop == 'majorMicrospecies':
			return MajorMicrospecies()
		elif prop == 'tautomerization':
			return Tautomerization()
		elif prop == 'stereoisomer':
			return Stereoisomer()
		elif prop == 'solubility':
			return Solubility()
		elif prop == 'logP':
			return LogP()
		elif prop == 'logD':
			return LogD()
		else:
			pass

class Pka(JchemProperty):
	def __init__(self):
		JchemProperty.__init__(self)
		self.name = 'pKa'
		self.url = '/webservices/rest-v0/util/calculate/pKa'
		self.postData = {
			"pHLower": 0.0,
			"pHUpper": 14.0,
			"pHStep": 0.1,
			"temperature": 298.0,
			"micro": False,
			"considerTautomerization": True,
			"pKaLowerLimit": -20.0,
			"pKaUpperLimit": 10.0,
			"prefix": "DYNAMIC"
		}

	def getMostAcidicPka(self):
		"""
		Picks out pKa acidic value(s), returns list
		"""
		pkaValList = []
		if 'mostAcidic' in self.results:
			# logging.info("$ type: {} $".format(self.results['mostAcidic']))
			for pkaVal in self.results['mostAcidic']:
				pkaValList.append(pkaVal)
			return pkaValList
		else:
			logging.warning("key: 'mostAcidic' not in self.results")
			return None

	def getMostBasicPka(self):
		"""
		Picks out pKa Basic value(s), returns list
		"""
		pkaValList = []
		if 'mostBasic' in self.results:
			for pkaVal in self.results['mostBasic']:
				pkaValList.append(pkaVal)
			return pkaValList
		else:
			logging.warning("no key 'mostBasic' in results")
			return None

	def getParent(self):
		"""
		Gets parent image from result and adds structure
		info such as formula, iupac, mass, and smiles.
		Returns dict with keys: image, formula, iupac, mass, and smiles
		"""
		try:
			parentDict = {'image': self.results['result']['image']['image']}
			parentDict.update(getStructInfo(self.results['result']['structureData']['structure']))
			return parentDict
		except KeyError as ke:
			logging.warning("key error: {}".format(ke))
			return None

	def getMicrospecies(self):
		"""
		Gets microspecies from pKa result and appends 
		structure info (i.e., formula, iupac, mass, and smiles)
		Returns list of microspeceies as dicts
		with keys: image, formula, iupac, mass, and smiles
		"""
		if 'microspecies' in self.results:
			msList = []
			for ms in self.results['microspecies']:
				msStructDict = {} # list element in msList
				msStructDict.update({'image': ms['image']['image'], 'key': ms['key']})
				structInfo = getStructInfo(ms['structureData']['structure'])
				msStructDict.update(structInfo)
				msList.append(msStructDict)
			return msList
		else:
			logging.info("no microspecies in results")
			return None

	def getChartData(self):
		if 'chartData' in self.results:
			microDistData = {} # microspecies distribution data 
			for ms in self.results['chartData']:
				valuesList = [] # format: [[ph1,con1], [ph2, con2], ...] per ms
				for vals in ms['values']:
					xy = [] # [ph1, con1]
					xy.append(vals['pH'])
					xy.append(100.0 * vals['concentration']) # convert to %
					valuesList.append(xy)
				microDistData.update({ms['key'] : valuesList})
			return microDistData
		else:
			return None


class IsoelectricPoint(JchemProperty):
	def __init__(self):
		JchemProperty.__init__(self)
		self.name = 'isoelectricPoint'
		self.url = '/webservices/rest-v0/util/calculate/isoelectricPoint'
		self.postData = {
    		"pHStep": 0.1,
			"doublePrecision": 2
		}

	def getIsoelectricPoint(self):
		"""
		Returns isoelectricPoint value from results
		"""
		try:
			return self.results['isoelectricPoint']
		except KeyError:
			logging.warning("key 'isoelectricPoint' not in results")
			return None

	def getIsoPtChartData(self):
		"""
		Returns isoelectricPoint chart data
		"""
		# isoPtChartData = {'isoPtChartData': None}
		valsList = []
		try:
			for pt in self.results['chartData']['values']:
				xyPair = []
				for key, value in pt.items():
					xyPair.append(value)
				valsList.append(xyPair)
		except KeyError as ke:
			logging.warning("key error: {}".format(ke))
			return valsList
		else:
			# isoPtChartData['isoPtChartData'] = valsList
			return valsList

class MajorMicrospecies(JchemProperty):
	def __init__(self):
		JchemProperty.__init__(self)
		self.name = 'majorMicrospecies'
		self.url = '/webservices/rest-v0/util/calculate/majorMicrospecies'
		self.postData = {
    		"pH": 7.4,
			"takeMajorTautomericForm": False
		}

	def getMajorMicrospecies(self):
		majorMsDict = {}
		try:
			majorMsDict.update({'image': self.results['result']['image']['image']})
			structInfo = getStructInfo(self.results['result']['structureData']['structure'])
			majorMsDict.update(structInfo) # add smiles, iupac, mass, formula key:values
			return majorMsDict
		except KeyError as ke:
			logging.warning("key error: {}".format(ke))
			return None

class Tautomerization(JchemProperty):
	def __init__(self):
		JchemProperty.__init__(self)
		self.name = 'tautomerization'
		self.url = '/webservices/rest-v0/util/calculate/tautomerization'
		self.postData = {
			"calculationType": "DOMINANT",
			"maxStructureCount": 1000,
			"considerPH": False,
			"enableMaxPathLength": True,
			"maxPathLength": 4,
			"rationalTautomerGenerationMode": False,
			"singleFragmentMode": True,
			"protectAromaticity": True,
		    "protectCharge": True,
			"excludeAntiAromaticCompounds": True,
			"protectDoubleBondStereo": False,
			"protectAllTetrahedralStereoCenters": False,
			"protectLabeledTetrahedralStereoCenters": False,
			"protectEsterGroups": True,
			"ringChainTautomerizationAllowed": False
		}

	def getTautomers(self):
		tautDict = {'tautStructs': [None]}
		tautImageList = []
		try:
			for taut in self.results['result']:
				tautStructDict = {'image': taut['image']['image']}
				structInfo = getStructInfo(taut['structureData']['structure'])
				tautStructDict.update(structInfo)
				tautStructDict.update({'dist': 100 * round(taut['dominantTautomerDistribution'], 4)})
				tautImageList.append(tautStructDict)
			tautDict.update({'tautStructs': tautImageList})
			return tautImageList
		except KeyError as ke:
			logging.warning("key error: {}".format(ke))
			return None

class Stereoisomer(JchemProperty):
	def __init__(self):
		JchemProperty.__init__(self)
		self.name = 'stereoisomer'
		self.url = '/webservices/rest-v0/util/calculate/stereoisomer'
		self.postData = {
			"stereoisomerismType": "TETRAHEDRAL",
			"maxStructureCount": 100,
			"protectDoubleBondStereo": False,
			"protectTetrahedralStereo": False,
			"filterInvalid3DStructures": False
		}

	def getStereoisomers(self):
		stereoList = []
		try:
			for stereo in self.results['result']:
				stereoDict = {'image': stereo['image']['image']}
				structInfo = getStructInfo(stereo['structureData']['structure'])
				stereoDict.update(structInfo)
				stereoList.append(stereoDict)
			return stereoList
		except KeyError as ke:
			logging.warning("key error: {}".format(ke))
			return None


class Solubility(JchemProperty):
	def __init__(self):
		JchemProperty.__init__(self)
		self.name = 'solubility'
		self.url = '/webservices/rest-v0/util/calculate/solubility'
		self.postData = {
			"pHLower": 0.0,
			"pHUpper": 14.0,
			"pHStep": 0.1,
			"unit": "MGPERML"
		}

	def getSolubility(self):
		"""
	    Gets water solubility for chemaxon
	    """
		try:
			return 1000.0 * self.results['intrinsicSolubility']
		except KeyError as ke:
			logging.warning("key error: {}".format(ke))
			return None


class LogP(JchemProperty):
	def __init__(self):
		JchemProperty.__init__(self)
		self.name = 'logP'
		self.url = '/webservices/rest-v0/util/calculate/logP'
		self.postData = {
			"method": "WEIGHTED",
			"wVG": 1.0,
			"wKLOP": 1.0,
			"wPHYS": 1.0,
			"Cl": 0.1,
			"NaK": 0.1,
			"considerTautomerization": False
		}

	def getLogP(self):
		"""
	    Gets pH-independent kow
	    """
		try:
			return self.results['logpnonionic']
		except KeyError as ke:
			logging.warning("ker error: {}".format(ke))
			return None


class LogD(JchemProperty):
	def __init__(self):
		JchemProperty.__init__(self)
		self.name = 'logD'
		self.url = '/webservices/rest-v0/util/calculate/logD'
		self.postData = {
			"pHLower": 0.0,
			"pHUpper": 14.0,
			"pHStep": 0.1,
			"method": "WEIGHTED",
			"wVG": 1.0,
			"wKLOP": 1.0,
			"wPHYS": 1.0,
			"Cl": 0.1,
			"NaK": 0.1,
			"considerTautomerization": False
		}

	def getLogD(self, ph):
		"""
	    Gets pH-dependent kow
	    """
		try:
			ph = float(ph)
			chartDataList = self.results['charData']['values']
			for xyPair in chartDataList:
				if xyPair['pH'] == round(ph, 1):
					value = xyPair['logD']
					break
			return value
		except KeyError as ke:
			logging.warning("key error: {}".format(ke))
			return None
	       

def doc(request):
	"""
	API Documentation Page
	"""
	return render(request, 'jchem_docs.html')


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
			addH = True
	else:
		if 'addH' in request.data:
			addH = True
	finally:
		# logging.info("chemical: {}".format(chem))
		ds = Data_Structures()
		data = ds.chemDeatsStruct(chem, addH) # format request to jchem
		data = json.dumps(data) # convert dict to json string
		# logging.info("data: {}".format(data))
		# logging.info("data type: {}".format(type(data)))
		url = Urls.jchemBase + Urls.detailUrl
		# logging.info("url: {}".format(url))
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
	request = {
		"structures": [
			{"structure": smiles}
		],
		"display": {
			"include": ["image"],
			"parameters": {
				"image": {
					# "width": imageWidth,
					# "height": imageHeight
					"scale": imgScale
				}
			}
		}
	}
	if imgHeight != None:
		request['display']['parameters']['image'].update({"width":imgWidth, "height":imgHeight})
	data = json.dumps(request) # to json string
	url = Urls.jchemBase + Urls.detailUrl
	imgData = web_call(url, request, data) # get response from jchem ws
	return imgData # return dict of image data


def mrvToSmiles(request):
	"""
	mrvToSmiles

	Inputs: chemical as mrv 
	Returns: SMILES string of chemical
	"""
	# queryDict = request.POST
	chemStruct = request.data.get('chemical') # chemical in <cml> format (marvin sketch)
	request = {
		"structure" : chemStruct,
		"inputFormat" : "mrv",
		"parameters" : "smiles"
	}
	data = json.dumps(request) # serialize to json-formatted str
	url = Urls.jchemBase + Urls.exportUrl
	smilesData = web_call(url, request, data) # get responset))
	return smilesData


def getChemSpecData(request):
	"""
	getChemSpecData

	Gets pKa values and microspecies distribution
	for a given chemical

	Inputs - data types to get (e.g., pka, tautomer, etc.),
	and all the fields from the 3 tables.
	"""
	ds = Data_Structures()
	addH = False
	if 'addH' in request.data:
		addH = True
	data = ds.chemSpecStruct(request.data, addH) # format request to jchem
	data = json.dumps(data)
	url = Urls.jchemBase + Urls.detailUrl
	results = web_call(url, request, data)
	return results


def getTransProducts(request):
	"""
	Makes request to metabolizer on cgi server
	"""
	url = Urls.metabolizerUrl
	data = json.dumps(request.POST)
	results = web_call(url, request, data)
	return results


def standardizer(request):
	"""
	Standardizes a structure in any format 
	recognized by Marvin, and the actions to
	perfrom on the structure (e.g., aromatize, daromatize,
	clear stereo, tautomerize, add explicit H, remove
	explicit H, transform, and neutralize). 

	NOTE: Just AddExplicitH and Aromatize configs for now.

	Returns molecule in mrv format
	"""
	url = Urls.jchemBase + Urls.standardizerUrl
	structure = request.POST.get('chemical')
	getConfig = request.POST.get('config')
	stdTmpl = """
	<?xml version="1.0" encoding="UTF-8"?>
	<StandardizerConfiguration>
		<Actions>
			<{{stdConfig}} ID="{{stdConfig}}"/>
		</Actions>
	</StandardizerConfiguration>
	"""
	stdData = Template(stdTmpl).render(Context(dict(stdConfig=getConfig)))
	stdData = stdData.replace('\n', '').replace('\r', '').replace('\t', '')
	data = {
		"structure": structure,
		"parameters": {
        	"standardizerDefinition": stdData
    	}
	}
	data = json.dumps(data)
	results = web_call(url, request, data)
	return results


def hydrogenizer(request):
	"""
	Addition or removal of explicit 
	hydrogens or lone pairs
	Inputs: chemical, method (e.g., HYDROGENIZE)
	Returns: molecule in mrv format 
	"""
	url = Urls.jchemBase + Urls.hydroUrl
	structure = request.POST.get('chemical')
	method = request.POST.get('method')
	data = {
		"structure": structure,
		"parameters": {
			"method": method
		}
	}
	data = json.dumps(data) # convert to json string
	results = web_call(url, request, data)
	return results


def getpchemprops(request):
	"""
	Calls pchemprop model to get pchem props 
	for a given molecule. This ws was
	originally meant for getting pchem props 
	for metabolites on the gentrans output page.

	This is only here for accessing pchemprop_model
	via frontend ajax calls
	"""
	from models.pchemprop import pchemprop_output
	pchemprop_obj = pchemprop_output.pchempropOutputPage(request) # run model (pchemprop_[output, model])

	# logging.info("pchemprop attributes: {}".format(dir(pchemprop_obj)))

	data = json.dumps({"checkedCalcsAndProps": pchemprop_obj.checkedCalcsAndPropsDict, 
						"chemaxonResults": pchemprop_obj.chemaxonResultsDict})
	# return requests.Response(content=data, content_type="application/json")
	return HttpResponse(data, content_type="application/json")


def getStructInfo(structure):
	"""
	Appends structure info to image url
	Input: structure in .mrv format
	Output: dict with structure's info (i.e., formula, iupac, mass, smiles),
	or dict with aforementioned keys but None values
	"""
	logging.info("STRUCTURE: {}".format(structure))
	# response = mrvToSmiles(requests.Request(data={'chemical': structure}))
	# smilesDict = json.loads(response.content)

	# logging.info("structure response: {}".format(smilesDict))

	request = requests.Request(data={"chemical": structure, "addH": True})
	# request = requests.Request(data={"chemical": smilesDict["structure"], "addH": True})
	response = getChemDetails(request)
	structDict = json.loads(response.content)

	infoDictKeys = ['formula', 'iupac', 'mass', 'smiles']
	infoDict = {key: None for key in infoDictKeys} # init dict with infoDictKeys and None vals
	struct_root = {} # root of data in structInfo
	if 'data' in structDict:
		struct_root = structDict['data'][0]
		infoDict.update({"formula": struct_root['formula']})
		infoDict.update({"iupac":  struct_root['iupac']})
		infoDict.update({"mass":  struct_root['mass']})
		infoDict.update({"smiles":  struct_root['smiles']})
	return infoDict


def web_call(url, request, data):
	"""
	Makes the request to a specified URL
	and POST data. Returns an http response.
	"""
	try:
		logging.info("making call...")
		logging.info("url: {}".format(url))
		response = requests.post(url, data=data, headers=headers, timeout=60)
		logging.info("received response: {}".format(response.content))
		return response
	except Exception as e:
		logging.warning("error at web call: {}".format(e))
		raise 


class Data_Structures:

	def chemDeatsStruct(self, chemical, addH=False):
		# return json data for chemical details
		chemDeatsDict =  {
			"structures": [
				{ "structure": chemical }
			],
			"display": {
				"include": [
					"structureData"
				],
				"additionalFields": {
					"formula": "chemicalTerms(formula)",
					"iupac": "chemicalTerms(name)",
					"mass": "chemicalTerms(mass)",
					"smiles": "chemicalTerms(molString('smiles'))",
				},
				"parameters": {
					"structureData": "mrv"
				}
			}
		}
		if addH:
			chemDeatsDict = addExplicitH(chemDeatsDict)
		return chemDeatsDict


	def chemSpecStruct(self, dic, addH=False):

		# don't forget about pKa_decimal

		keys = ["isoelectricPoint", "pKa", "majorMicrospecies", "stereoisomer", 
				"tautomerization", "logP", "logD", "solubility"]

		structures = []
		if 'chemical' in dic:
			structures = [{"structure": dic["chemical"]}]

		includeList = []
		paramsDict = {} # dict of dict where latter dict has key of param and vals of param vals

		for key, value in dic.items():
			if key in keys:
				includeList.append(key) # add parameter to "include" list
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


def gen_jid():
    ts = datetime.datetime.now(pytz.UTC)
    localDatetime = ts.astimezone(pytz.timezone('US/Eastern'))
    jid = localDatetime.strftime('%Y%m%d%H%M%S%f')
    return jid