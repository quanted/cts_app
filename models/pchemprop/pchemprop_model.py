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

n = 3 # number of decimal places to round values


class pchemprop(object):
	def __init__(self, run_type, chem_struct, smiles, name, formula, mass, chemaxon, epi, 
					test, sparc, measured, melting_point, boiling_point, water_sol, 
					vapor_press, mol_diss, ion_con, henrys_law_con, kow_no_ph, kow_wph, kow_ph, koc):

		self.run_type = run_type # defaults to "single", "batch" coming soon...
		self.jid = jchem_rest.gen_jid() # get time of run

		self.chem_struct = chem_struct
		self.smiles = smiles
		self.name = name
		self.formula = formula
		self.mass = mass

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
		self.measured = measured

		calcluatorsDict = {
			"chemaxon": self.chemaxon,
			"epi": self.epi,
			"test": self.test,
			"sparc": self.sparc,
			"measured": self.measured
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

		self.checkedCalcsAndPropsDict = checkedCalcsAndPropsDict

		# TODO: Make more general. getChemaxonResults() could probably be changed to loop
		# through all calculators. Also, establish standardized variable names to reduce
		# amount of code (e.g., conditionals checking prop values)
		self.chemaxonResultsDict = getChemaxonResults(self.chem_struct, checkedCalcsAndPropsDict, self.kow_ph)
		# self.testResultsDict = getTestResults(self.chem_struct, checkedCalcsAndPropsDict) # kow_wph not available
		# self.measuredResultsDict = getMeasuredResults(self.chem_struct, checkedCalcsAndPropsDict)

		self.resultsDict = {
			"chemaxon": self.chemaxonResultsDict,
			"epi-suite": None,
			"sparc": None,
			"test": None,
			"measured": None
		}

		self.rawData = self.chemaxonResultsDict

		# fileout = open('C:\\Documents and Settings\\npope\\Desktop\\out.txt', 'w')
		# fileout.write(json.dumps(self.rawData))
		# fileout.close()

		"""
		Sample TEST calls and stuff (add this to the model):
		"""
		# For the Measured column:
		# $.ajax({type: "GET", url: "/test_cts/api/TEST/"+$('#molecule').val()+"/MP/MEASURED", dataType: "json"}).done(function(val) { $('#id_melting_point_MEASURED').html(val.MEASURED.toPrecision(4)) } )
		# $.ajax({type: "GET", url: "/test_cts/api/TEST/"+$('#molecule').val()+"/BP/MEASURED", dataType: "json"}).done(function(val) { $('#id_boiling_point_MEASURED').html(val.MEASURED.toPrecision(4)) } )
		# $.ajax({type: "GET", url: "/test_cts/api/TEST/"+$('#molecule').val()+"/WS/MEASURED", dataType: "json"}).done(function(val) { $('#id_water_sol_MEASURED').html(val.MEASURED.toPrecision(4)) } )
		# $.ajax({type: "GET", url: "/test_cts/api/TEST/"+$('#molecule').val()+"/VP/MEASURED", dataType: "json"}).done(function(val) { $('#id_vapor_press_MEASURED').html(val.MEASURED.toPrecision(4)) } )
		# For the TEST column:
		# $.ajax({type: "GET", url: "/test_cts/api/TEST/"+$('#molecule').val()+"/MP", dataType: "json"}).done(function(val) { $('#id_melting_point_TEST').html(val.TEST.toPrecision(4)) } )
  		# $.ajax({type: "GET", url: "/test_cts/api/TEST/"+$('#molecule').val()+"/BP", dataType: "json"}).done(function(val) { $('#id_boiling_point_TEST').html(val.TEST.toPrecision(4)) } )
  		# $.ajax({type: "GET", url: "/test_cts/api/TEST/"+$('#molecule').val()+"/WS", dataType: "json"}).done(function(val) { $('#id_water_sol_TEST').html(val.TEST.toPrecision(4)) } )
  		# $.ajax({type: "GET", url: "/test_cts/api/TEST/"+$('#molecule').val()+"/VP", dataType: "json"}).done(function(val) { $('#id_vapor_press_TEST').html(val.TEST.toPrecision(4)) } )
  		# $.ajax({type: "GET", url: "/test_cts/api/TEST/"+$('#molecule').val()+"/MLOGP", dataType: "json"}).done(function(val) { $('#id_kow_no_ph_TEST').html(val.MLOGP.toPrecision(4)) } )


def getTestResults(structure, checkedCalcsAndPropsDict):
	"""
	Gets pchemprop data from TEST ws.
	Inputs: chemical structure, dict of checked properties by calculator
	(e.g., { 'test': ['kow_no_ph', 'melting_point'] })
	Returns: dict of TEST props in template-friendly format (see pchemprop_tables)
	"""

	url = "/test_cts/api/TEST/" + structure
	testPropsList = checkedCalcsAndPropsDict.get('test', None)

	if testPropsList:
		testValues = {}
		for prop in testPropsList:
			if prop == "melting_point":
				testValues.update({prop: requests.get(url + "/MP")})
			elif prop == "boiling_point":
				testValues.update({prop: requests.get(url + "/BP")})
			elif prop == "water_sol":
				testValues.update({prop: requests.get(url + "/WS")})
			elif prop == "vapor_press":
				testValues.update({prop: requests.get(url + "/VP")})
		return testValues
	else: return None


def getMeasuredResults(structure, checkedCalcsAndPropsDict):
	"""
	Gets pchemprop data from measured ws.
	Inputs: chemical structure, dict of checked properties by calculator
	(e.g., { 'measured': ['kow_no_ph', 'melting_point'] })
	Returns: dict of measured props in template-friendly format (see pchemprop_tables)
	"""

	url = "/test_cts/api/TEST/" + structure
	measuredPropsList = checkedCalcsAndPropsDict.get('measured', None)

	if measuredPropsList:
		measuredValues = {}
		for prop in measuredPropsList:
			if prop == "melting_point":
				measuredValues.update({prop: requests.get(url + "/MP/MEASURED")})
			elif prop == "boiling_point":
				measuredValues.update({prop: requests.get(url + "/BP/MEASURED")})
			elif prop == "water_sol":
				measuredValues.update({prop: requests.get(url + "/WS/MEASURED")})
			elif prop == "vapor_press":
				measuredValues.update({prop: requests.get(url + "/VP/MEASURED")})
			elif prop == "kow_no_ph":
				measuredResponse = requests.get(url + "/MLOGP/MEASURED")
		return measuredValues
	else: return None


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
				chemaxonDict.update({"Water Solubility": data})
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
				chemaxonDict.update({"Ionization Constant": data})
			if prop == "kow_no_ph":
				chemaxonDict.update({"Octanol/Water Partition Coefficient": {}})
				for method in propMethodsList:
					postDict = {
						"chemical": structure,	
						"logP": {
							"method": method
						}
					}
					data = json.loads(makeJchemCall(postDict))
					chemaxonDict["Octanol/Water Partition Coefficient"].update({method: data})
				
			if prop == "kow_wph":
				chemaxonDict.update({"Octanol/Water Partition Coefficient at pH": {}})
				for method in propMethodsList:
					postDict = {
						"chemical": structure,
						"logD": {
							"method": method,
							"pHLower": 0,
							"pHUpper": 14,
							"pHStep": 0.1
						}
					}
					data = json.loads(makeJchemCall(postDict))
					chemaxonDict["Octanol/Water Partition Coefficient at pH"].update({method: data})

		# fileout = open('C:\\Documents and Settings\\npope\\Desktop\\out.txt', 'w')
		# fileout.write(json.dumps(chemaxonDict))
		# fileout.close()
		return chemaxonDict



		# jchem ws only accepts on method at a time
		# for method in propMethodsList:
		# 	postDict = {"chemical": structure}
		# 	# loop through chemaxon properties
		# 	for prop in chemaxonPropsList:
		# 		if prop == "solubility":
		# 			postDict.update({
		# 				# "chemical": structure,
		# 				"solubility": {
		# 					"pHLower": 0,
		# 					"pHUpper": 14,
		# 					"pHStep": 0.1,
		# 					"unit": "LOGS"
		# 				}
		# 			})
		# 		if prop == "ion_con":
		# 			# make call to getChemSpecData() for pKa values
		# 			postDict.update({
		# 				"chemical": structure,
		# 				"pKa": { 
		# 					"pHLower": 0, # note: default values
		# 					"pHUpper": 14,
		# 					"pHStep": 0.1
		# 				}
		# 			})
		# 		if prop == "kow_no_ph":
		# 			postDict.update({
		# 				"logP": {
		# 					"method": method
		# 				}
		# 			})
		# 		if prop == "kow_wph":
		# 			postDict.update({
		# 				"logD": {
		# 					"method": method,
		# 					"pHLower": 0,
		# 					"pHUpper": 14,
		# 					"pHStep": 0.1
		# 				}
		# 			})

			# if postDict != None:
			# 	request = HttpRequest()
			# 	request.POST = postDict
			# 	response = jchem_rest.getChemSpecData(request)
			# 	chemaxonDict.update({method: json.loads(response.content)}) # results per method dictionary


		# return buildChemaxonResultsDict(chemaxonDict, phForLogD)


def buildChemaxonResultsDict(chemaxonDict, phForLogD):
	"""
	Parses results from chemaxon data call and
	returns a dictionary in a format recognized 
	by the template in pchemprop_tables.py

	Inputs: chemaxon dict, pH for logD (if selected)
	Returns: dictionary of chemaxon values for output page
	"""

	propDict = {}

	# loop through results per method
	for method, result in chemaxonDict.items():

		root = result['data'][0]

		# logging.warning(root)

		if 'pKa' in root:
			# get mostAcidic and mostBasic values (both are list)
			pkaList = []
			for val in root['pKa']['mostAcidic']:
				pkaList.append(round(val, n))
			pkbList = []
			for val in root['pKa']['mostBasic']:
				pkbList.append(round(val, n))

			if 'Ionization Constant' in propDict:
				propDict['Ionization Constant'].update({
					method: {
						"pKa": pkaList,
						"pKb": pkbList
					}
				})
			else:
				propDict.update({
					"Ionization Constant": {
						method: {
							"pKa": pkaList,
							"pKb": pkbList
						} 
					}
				})

		dataDict = {}
		structInfo = {}
		if 'logP' in root:
			logPkeys = ['logpnonionic', 'logdpi', 'structInfo']
			logPname = "Octanol/Water Partition Coefficient"
			# get logpnonionic, logdpi, and imageUrl
			if 'logpnonionic' in root['logP'] and not isinstance(root['logP']['logpnonionic'], dict):
				dataDict.update({
					"logpnonionic": round(root['logP']['logpnonionic'], n)
				})
			else:
				dataDict.update({
					"logpnonionic": "none"
				})

			# if 'logdpi' in root['logP'] and not isinstance(root['logP']['logdpi'], dict):
			# 	dataDict.update({
			# 		"logdpi": round(root['logP']['logdpi'], n)
			# 	})
			# else:
			# 	dataDict.update({
			# 		"logdpi": "none"
			# 	})

			# if 'result' in root['logP']:
			# 	if 'structureData' in root['logP']['result']:
			# 		# Get smiles, iupac, mass, etc. as dict for logP structure
			# 		# TODO: move getStructInfo() to more generic place. it's used in all workflows
			# 		structInfo = chemspec_model.getStructInfo(root['logP']['result']['structureData']['structure'])
			# 		dataDict[logPname].update({'structInfo': structInfo})
			# 	if 'image' in root['logP']['result']:
			# 		dataDict.update({
			# 			"image": root['logP']['result']['image']['imageUrl']
			# 		})

			if logPname in propDict:
				propDict[logPname].update({
					method: dataDict 
				})
			else:
				propDict.update({
					logPname: {
						method: dataDict
					}
				})

		if 'logD' in root:
			logDname = "Octanol/Water Partition Coefficient at pH"
			if 'logD' in root['logD']:

				phForLogD = float(phForLogD) # convert to float
				chartDataList = root['logD']['chartData']['values'] # list of {"pH":val, "logD":val}

				for xyPair in chartDataList:
					# use value at pH requested by user
					if xyPair['pH'] == round(phForLogD, 1):
						logDval = xyPair['logD']
						break

				if logDname in propDict:
					propDict[logDname].update({
						method: {
							"logD": round(logDval, n)
						}
					})
				else:
					propDict.update({
						logDname: {
							method: {
								"logD": round(logDval, n)
							}
						}
					})

	return propDict


def makeJchemCall(postDict):
	request = HttpRequest()
	request.POST = postDict
	response = jchem_rest.getChemSpecData(request)
	return response.content