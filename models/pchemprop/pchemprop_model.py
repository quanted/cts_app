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


class pchemprop(object):
	def __init__(self, run_type, chem_struct, smiles, name, formula, mass, chemaxon, epi, 
					test, sparc, measured, melting_point, boiling_point, water_sol, 
					vapor_press, mol_diss, ion_con, henrys_law_con, kowNoPh, kowWph, kowPh, koc):

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
		self.kowNoPh = kowNoPh
		self.kowWph = kowWph
		self.kowPh = kowPh
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
			"kow_no_ph": self.kowNoPh,
			"kow_wph": self.kowWph,
			"kow_ph": self.kowPh,
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

		logging.warning(checkedCalcsAndPropsDict)
		self.checkedCalcsAndPropsDict = checkedCalcsAndPropsDict

		chemaxonPostData = buildChemaxonRequest(self.chem_struct, checkedCalcsAndPropsDict)
		self.rawData = makeRequest(chemaxonPostData)

		# fileout = open('C:\\Documents and Settings\\npope\\Desktop\\out.txt', 'w')
		# fileout.write(self.rawData)
		# fileout.close()

		chemaxonResultsDict = json.loads(self.rawData) # convert to dictionary

		# get results from json:
		self.chemaxonResultsDict = getChemaxonResults(chemaxonResultsDict)


def buildChemaxonRequest(structure, checkedCalcsAndPropsDict):
	"""
	Input: dict of checked/available properties for calculators
	Returns: dict of chemaxon props in web-service-friendly format
	"""

	chemaxonPropsList = checkedCalcsAndPropsDict.get('chemaxon', None)

	if chemaxonPropsList:
		postDict = {}
		for prop in chemaxonPropsList:

			logging.warning("prop: " + str(prop))

			# loop through props in list
			if prop == "ion_con":
				# make call to getChemSpecData() for pKa values
				postDict.update({
					"chem_struct": structure,
					"pKa": { 
						"pHLower":0, # note: default values
						"pHUpper":14,
						"pHStep":0.1
					}
				})
			if prop == "kow_no_ph":
				postDict.update({
					"logP": {
						"method": "WEIGHTED" #TODO: loop through all methods for all props
					}
				})
			if prop == "kow_wph":
				postDict.update({
					"logD": {
						"method": "WEIGHTED",
					}
				})

		return postDict


def getChemaxonResults(chemaxonDict):

	chemaxonRoot = chemaxonDict['data'][0]

	chemaxonKeys = ['pKa', 'logP', 'logD']
	dataDict = {key: None for key in chemaxonKeys}
	
	if 'pKa' in chemaxonRoot:
		# get mostAcidic and mostBasic values (both list)
		pkaList = []
		for val in chemaxonRoot['pKa']['mostAcidic']:
			pkaList.append(val)
		pkbList = []
		for val in chemaxonRoot['pKa']['mostBasic']:
			pkbList.append(val)

		dataDict['pKa'] = {
			"mostAcidic": pkaList,
			"mostBasic": pkbList
		}

	if 'logP' in chemaxonRoot:
		dataDict['logP'] = {}
		# get logpnonionic, logdpi, and imageUrl
		if 'logpnonionic' in chemaxonRoot['logP'] and not isinstance(chemaxonRoot['logP']['logpnonionic'], dict):
			dataDict['logP'].update({
				"logpnonionic": chemaxonRoot['logP']['logpnonionic']
			})
		if 'logdpi' in chemaxonRoot['logP'] and not isinstance(chemaxonRoot['logP']['logdpi'], dict):
			dataDict['logP'].update({
				"logdpi": chemaxonRoot['logP']['logdpi']
			})
		if 'result' in chemaxonRoot['logP']:
			if 'image' in chemaxonRoot['logP']['result']:
				dataDict['logP'].update({
					"image": chemaxonRoot['logP']['result']['image']['imageUrl']
				})
			if 'structureData' in chemaxonRoot['logP']['result']:
				# Get smiles, iupac, mass, etc. as dict for logP structure
				# TODO: move getStructInfo() to more generic place. it's used in all workflows
				structInfo = chemspec_model.getStructInfo(chemaxonRoot['logP']['result']['structureData']['structure'])
				dataDict['logP'].update(structInfo)

	if 'logD' in chemaxonRoot:
		dataDict['logD'] = {}
		if 'logD' in chemaxonRoot['logD']:
			dataDict['logD'].update({"logD": chemaxonRoot['logD']['logD']})

	return dataDict


def makeRequest(postData):
	"""
	Makes request to jchem-cts ws
	Input: post data as dict
	Returns: response content (json string)
	"""
	request = HttpRequest()
	request.POST = postData
	response = jchem_rest.getChemSpecData(request)
	return response.content