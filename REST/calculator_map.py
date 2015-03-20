###########################################################
# Herein lies the map to the various calculators' queries #
###########################################################

import requests
import jchem_rest


class Calculator(object):
	"""
	Skeleton class for calculators

	NOTE: molID is recycled, always use "7"
	"""
	def __init__(self):
		self.name = ''
		self.propMap = {} # expecting list
		self.baseUrl = ''
		self.urlStruct = ''
		self.baseUrl = ''

	@classmethod
	def getCalcObject(self, calc):
		if calc == 'chemaxon':
			return ChemaxonCalc()
		elif calc == 'test':
			return TestCalc()
		elif calc == 'epi':
			return EpiCalc()
		elif calc == 'measured':
			return MeasuredCalc()
		else:
			raise TypeError('Valid calculators are chemaxon, test, epi, and measured')

	def getUrl(self, molID, propKey, method=None):
		if propKey in self.propMap:
			calcProp = self.propMap[propKey]['urlKey']
			if self.name == 'test':
				if method: 
					return self.urlStruct.format(molID, calcProp, method)
				else: 
					return "Error: TEST must have a method in the argument"
			else: 
				return self.urlStruct.format(molID, calcProp)
		else: 
			return "Error: key not found"

	def getResultKey(self, propKey):
		if propKey in self.propMap:
			return self.propMap[propKey]['resultKey']
		else:
			return "Error: key not found"


class TestCalc(Calculator):
	"""
	TEST Calculator
	"""
	def __init__(self):

		Calculator.__init__(self)

		self.urlStruct = "/test/test/calc/{}/{}/{}" # molID, propKey, method
		self.methods = ['hierarchical'] # accounting for one method atm
		self.name = "test"
		self.baseUrl = "http://134.67.114.6/"
		self.propMap = {
			'melting_point': {
				'urlKey': 'meltingPoint',
				'resultKey': 'meltingPointTESTHierarchical',
			},
			'boiling_point': {
				'urlKey': 'boilingPoint',
				'resultKey': 'boilingPointTESTHierarchical'
			},
			'water_sol': {
				'urlKey': 'waterSolubility',
				'resultKey': 'waterSolubilityTESTHierarchical'
			},
			'vapor_press': {
				'urlKey': 'vaporPressure',
				'resultKey': 'vaporPressureTESTHierarchical'
			}
		}

	def getPchemPropData(self, propKey):
		try:
			if propKey in self.propMap:
				req = requests.Request(data={'calc': 'test', 'prop': propKey})
				return test_cts.views.less_simple_proxy(req)
			else:
				raise # ?
		except KeyError:
			print "Property does not exist in TEST"


class EpiCalc(Calculator):
	"""
	EPI Suite Calculator
	"""

	def __init__(self):

		Calculator.__init__(self)

		self.name = "epi"
		self.urlStruct = "/test/epi/calc/{}/{}" # molID, propKey
		self.methods = None
		self.baseUrl = "http://134.67.114.6/"
		self.propMap = {
			'melting_point': {
				'urlKey': 'meltingPtDegCEstimated',
				'resultKey': 'meltingPtDegCEstimated'
			},
			'boiling_point': {
				'urlKey': 'boilingPtDegCEstimated',
				'resultKey': 'boilingPtDegCEstimated'
			},
			'water_sol': {
				'urlKey': 'waterSolMgLEstimated',
				'resultKey': 'waterSolMgLEstimated'
			},
			'vapor_press': {
				'urlKey': 'vaporPressMmHgEstimated',
				'resultKey': 'vaporPressMmHgEstimated'
			},
			'henrys_law_con': {
				'urlKey': 'henryLcBondAtmM3Mole',
				'resultKey': 'henryLcBondAtmM3Mole'
			},
			'kow_no_ph': {
				'urlKey': 'logKowEstimate',
				'resultKey': 'logKowEstimate'
			},
		}


class MeasuredCalc(Calculator):
	"""
	Measured Data (technically not a calculator)
	"""

	def __init__(self):

		Calculator.__init__(self)

		self.urlStruct = "/test/measured/{}/test/{}" # molID, propKey
		self.methods = None
		self.baseUrl = "http://134.67.114.6/"
		self.propMap = {
			'melting_point': {
				'urlKey': 'meltingPoint',
				'resultKey': 'measuredMeltingPoint',
			},
			'boiling_point': {
				'urlKey': 'boilingPoint',
				'resultKey': 'measuredBoilingPoint'
			},
			'water_sol': {
				'urlKey': 'waterSolubility',
				'resultKey': 'measuredWaterSolubility'
			},
			'vapor_press': {
				'urlKey': 'vaporPressure',
				'resultKey': 'measuredVaporPressure'
			}
		}


class ChemaxonCalc(Calculator):
	"""
	ChemAxon Calculator

	Starting out as its own class, then if it makes
	sense I'll integrate it into the Calculator class
	"""

	def __init__(self):

		Calculator.__init__(self)

		metabolizerUrl = "/efsws/rest/metabolizer" # TODO: figure out better book keeping for urls 
		jchemUrl = "/webservices/rest-v0/util/{}/{}"

		self.name = "chemaxon"

		# NOTE: would it make sense to map urlKeys to jchem_rest functions?
		# Or do another way I haven't thought of yet?
		self.propMap = {
			'water_sol': {
				'urlKey': '',
				'resultKey': ''
			},
			'ion_con': {
				'urlKey': '',
				'resultKey': ''
			},
			'kow_no_ph': {
				'urlKey': '',
				'resultKey': '',
				'methods': ['KLOP', 'VG', 'PHYS']
			},
			'kow_wph': {
				'urlKey': '',
				'resultKey': '',
				'methods': ['KLOP', 'VG', 'PHYS']
			}
		}

	def getPostDataForProp(prop, structure, method=None, phForLogD=None):
		postData = {}
		if prop == 'water_sol':
			postData = {
				"chemical": structure,
				"solubility": {
					"pHLower": 0,
					"pHUpper": 14,
					"pHStep": 0.1,
					"unit": "MGPERML"
				}
			}
		elif prop == 'ion_con':
			postData = {
				"chemical": structure,
				"pKa": { 
					"pHLower": 0,
					"pHUpper": 14,
					"pHStep": 0.1
				}
			}
		elif prop == 'kow_no_ph':
			postData = {
				"chemical": structure,	
				"logP": {
					"method": method
				}
			}
		elif prop == 'kow_wph':
			postData = {
				"chemical": structure,
				"logD": {
					"method": method,
					"pHLower": phForLogD,
					"pHUpper": phForLogD,
					"pHStep": 0.1
				}
			}
		return postData

	def getPchemPropData(self, propKey):
		try:
			if propKey in self.propMap:
				req = requests.Request(data=getPostDataForProp(propKey))
				res = jchem_rest.getChemSpecData(req) # send request to jchem_rest
				return res
			else:
				raise
		except KeyError:
			print "Property does not exist in ChemAxon"
		