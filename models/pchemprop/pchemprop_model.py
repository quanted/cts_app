"""
2014-08-13 (np)
"""

import urllib2
import json
import requests
import pchemprop_parameters # Chemical Calculator and Transformation Pathway parameters
from REST import jchem_rest
from django.http import HttpRequest
import logging
from models.chemspec import chemspec_model # for getStructInfo(), TODO: move func to more generic place
import decimal
import os


n = 3 # number of decimal places to round values


class pchemprop(object):
	def __init__(self, run_type, chem_struct, smiles, name, formula, mass, chemaxon, epi, 
					test, sparc, melting_point, boiling_point, water_sol, 
					vapor_press, mol_diss, ion_con, henrys_law_con, kow_no_ph, kow_wph, kow_ph, koc):

		self.run_type = run_type # defaults to "single", "batch" coming soon...
		self.jid = jchem_rest.gen_jid() # get time of run

		# chemical structure
		self.chem_struct = chem_struct
		self.smiles = smiles
		self.name = name
		self.formula = formula
		self.mass = mass + ' g/mol'

		# chemical properties (values 'on' or None) -- django params
		self.melting_point = melting_point
		self.boiling_point = boiling_point
		self.water_sol = water_sol
		self.vapor_press = vapor_press
		self.mol_diss = mol_diss
		self.ion_con = ion_con
		self.henrys_law_con = henrys_law_con
		self.kow_no_ph = kow_no_ph
		self.kow_wph = kow_wph
		self.kow_ph = kow_ph
		self.koc = koc

		# Create dictionary of chemprops with keys --> field names
		checkedPropsDict = {
			"melting_point": self.melting_point,
			"boiling_point": self.boiling_point,
			"water_sol": self.water_sol,
			"vapor_press": self.vapor_press,
			"mol_diss": self.mol_diss,
			"ion_con": self.ion_con,
			"henrys_law_con": self.henrys_law_con,
			"kow_no_ph": self.kow_no_ph,
			"kow_wph": self.kow_wph,
			"kow_ph": self.kow_ph,
			"koc": self.koc
		}

		# calcluators' checkboxes (values 'true' or None) -- static html from cts_pchem.html
		self.chemaxon = chemaxon
		self.epi = epi
		self.test = test
		self.sparc = sparc

		calcluatorsDict = {
			"chemaxon": chemaxon,
			"epi": epi,
			"test": test,
			"sparc": sparc
		}

		# dict with keys of checked calculators and values of 
		# checked properties that are also available for said calculators
		# format: { key: "calculator name", value: [checked property ids] }
		checkedCalcsAndPropsDict = {}
		for calcKey, calcValue in calcluatorsDict.items():
			if calcValue == 'true' or calcValue == 'on':
				# get checked parameters that are available for calculator
				propList = []
				for propKey, propValue in checkedPropsDict.items():
					# find checked properties
					if propValue == 'on' or propValue == 'true':
						# check if property is available for calculator:
						if pchemprop_parameters.pchempropAvailable(calcKey, propKey):
							propList.append(propKey)
				checkedCalcsAndPropsDict.update({calcKey:propList})

		# self.checkedCalcsAndPropsDict = checkedCalcsAndPropsDict

		# TODO: Make more general. getChemaxonResults() could probably be changed to loop
		# through all calculators. Also, establish standardized variable names to reduce
		# amount of code (e.g., conditionals checking prop values)
		chemaxonResultsDict = getChemaxonResults(self.chem_struct, checkedCalcsAndPropsDict, self.kow_ph)
		testResultsDict = getTestResults(self.chem_struct, checkedCalcsAndPropsDict)

		# self.testResultsDict = getTestResults(self.chem_struct, checkedCalcsAndPropsDict) # kow_wph not available
		# self.measuredResultsDict = getMeasuredResults(self.chem_struct, checkedCalcsAndPropsDict)

		self.resultsDict = {
			"chemaxon": chemaxonResultsDict,
			"epi": None,
			"sparc": None,
			"test": testResultsDict,
		}

		# logging.info(" ### Main Dictionary: {} ###".format(self.resultsDict))

		# self.rawData = self.chemaxonResultsDict

		# fileout = open('C:\\Documents and Settings\\npope\\Desktop\\out.txt', 'w')
		# fileout.write(json.dumps(self.rawData))
		# fileout.close()


def getTestResults(structure, checkedCalcsAndPropsDict):
	"""
	Gets pchemprop data from TEST ws.
	Inputs: chemical structure, dict of checked properties by calculator
	(e.g., { 'test': ['kow_no_ph', 'melting_point'] })
	Returns: dict of TEST props in template-friendly format (see pchemprop_tables)

	!!! TODO: Move this where it belongs: the test_cts app folder. Ultimately
	do the same for chemaxon and the other calculators !!!
	"""

	testMethodsList = ['fda', 'hierarchical', 'group', 'consensus', 'neighbor']

	url = ""
	if 'CTS_TEST_SERVER_INTRANET' in os.environ:
		url = os.environ['CTS_TEST_SERVER_INTRANET']
	else:
		url = os.environ['CTS_TEST_SERVER']

	baseUrl = url + "/test"
	# baseUrl = "http://a.ibdb.net/cts" #create molecule with id
	molUrl = "/molecules"

	testUrl = baseUrl + "/test/calc" #/test/calc/{id}/[property]/{method} method - fda, neighbor, and more!

	# give molecule an id to use for test calculations
	postData = {
		"id": 7,
		"smiles": str(structure)
	}	
	# response = makeTestCall(baseUrl + molUrl, postData) #already response.content
	response = requests.post(baseUrl + molUrl, data=json.dumps(postData), headers=headers)

	# logging.info(" ### POST Molecule Response: {} ### ".format(response))

	testPropsList = checkedCalcsAndPropsDict.get('test', None)

	testUrl += "/" + str(postData["id"]) # append id to test request

	if testPropsList:
		testValues = {}
		for prop in testPropsList:
			logging.info("inside prop loop")
			# testValues.update({prop: })
			for method in testMethodsList:
				if prop == "melting_point":
					testValues.update({prop: makeTestCall(testUrl + "/meltingPoint/" + method)})
				elif prop == "boiling_point":
					testValues.update({prop: makeTestCall(testUrl + "/boilingPoint/" + method)})
				elif prop == "water_sol":
					testValues.update({prop: makeTestCall(testUrl + "/waterSolubility/" + method)})
				elif prop == "vapor_press":
					testValues.update({prop: makeTestCall(testUrl + "/vaporPressure/" + method)})
		
		logging.info(" ### TEST Data Response: {} ### ".format(testValues))

		return testValues
	else: return None


headers = {'Content-Type' : 'application/json'}

def makeTestCall(url, postData=None):
	
	if postData:
		response = requests.post(url, data=postData, headers=headers)
	else:
		response = requests.get(url, headers=headers)

	# logging.info("--- RESPONSE: {} --- ".format(response.content))

	return response.content


def getChemaxonResults(structure, checkedCalcsAndPropsDict, phForLogD):
	"""
	Building the web call to make based on checked properties
	for chemaxon.

	Input: dict of checked/available properties for calculators
	Returns: dict of chemaxon props in template-friendly format
	"""

	chemaxonPropsList = checkedCalcsAndPropsDict.get('chemaxon', None)
	propMethodsList = ['KLOP', 'PHYS', 'VG'] # methods of calculation for pchemprops (chemaxon)

	if chemaxonPropsList:

		# propMethodsList = ['KLOP', 'PHYS', 'VG', 'WEIGHTED']
		chemaxonDict = {} # dict of results (values) per method (keys)

		# TODO: Some segments of the below repeat and could probably be looped..
		# change that at some point
		for prop in chemaxonPropsList:
			if prop == "solubility":
				postDict = {
					"chemical": structure,
					"solubility": {
						"pHLower": 0,
						"pHUpper": 14,
						"pHStep": 0.1,
						"unit": "LOGS"
					}
				}
				data = json.loads(makeJchemCall(postDict))
				chemaxonDict.update({"water_sol": data})
			if prop == "ion_con":
				postDict = {
					"chemical": structure,
					"pKa": { 
						"pHLower": 0, # note: default values
						"pHUpper": 14,
						"pHStep": 0.1
					}
				}
				data = json.loads(makeJchemCall(postDict))
				chemaxonDict.update({"ion_con": data})
			if prop == "kow_no_ph":
				chemaxonDict.update({prop: {}})
				for method in propMethodsList:
					postDict = {
						"chemical": structure,	
						"logP": {
							"method": method
						}
					}
					data = json.loads(makeJchemCall(postDict))
					chemaxonDict[prop].update({method: data})
				
			if prop == "kow_wph":
				chemaxonDict.update({prop: {}})
				for method in propMethodsList:
					postDict = {
						"chemical": structure,
						"logD": {
							"method": method,
							"pHLower": phForLogD,
							"pHUpper": phForLogD,
							"pHStep": 0.1
						}
					}
					data = json.loads(makeJchemCall(postDict))
					chemaxonDict[prop].update({method: data})

		return chemaxonDict


def makeJchemCall(postDict):
	request = HttpRequest()
	request.POST = postDict
	response = jchem_rest.getChemSpecData(request)
	return response.content