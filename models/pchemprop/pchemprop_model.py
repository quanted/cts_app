"""
2014-08-13 (np)
"""

import urllib2
import json
import requests
import pchemprop_parameters # Chemical Calculator and Transformation Pathway parameters
from REST import jchem_rest
from django.http import HttpRequest
from django.http import HttpResponse
import logging
from models.chemspec import chemspec_model # for getStructInfo(), TODO: move func to more generic place
import decimal
import os
import time

from REST import calculator_map as calcMap
from requests_futures.sessions import FuturesSession


n = 3 # number of decimal places to round values
requestCounter = 0 # yeah figure out a better way to do this...
totalRequest = 0 # total number of request. again, better way please


class pchemprop(object):
	def __init__(self, run_type, chem_struct, smiles, name, formula, mass, chemaxon, epi, 
					test, sparc, measured, melting_point, boiling_point, water_sol, 
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

		calcluatorsDict = {
			"chemaxon": chemaxon,
			"epi": epi,
			"test": test,
			"sparc": sparc,
			"measured": measured
		}

		# dict with keys of checked calculators and values of 
		# checked properties that are also available for said calculators
		# format: { key: "calculator name", value: [checked property ids] }
		self.checkedCalcsAndPropsDict = {}
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
				self.checkedCalcsAndPropsDict.update({calcKey:propList})

		# logging.info("CheckedCalcsAndProps: {}".format(self.checkedCalcsAndPropsDict))


		#####################################
		# initializeDB() # create table in db
		global requestCounter
		requestCounter = 0 # initialize request counter
		global totalRequest
		totalRequest = 0
		#####################################

		# logging.info("after db init")

		chemaxonResultsDict = getChemaxonResults(self.chem_struct, self.checkedCalcsAndPropsDict, self.kow_ph)
		testResultsDict = getTestResults(self.chem_struct, self.checkedCalcsAndPropsDict) # gets test, measured, and epi data

		logging.info("TEST Results: {}".format(testResultsDict))

		self.resultsDict = {
			"chemaxon": chemaxonResultsDict,
			"epi": None,
			# "epi": testResultsDict.get('epi', None),
			"sparc": None,
			"test": None,
			# "test": testResultsDict.get('test', None),
			"measured": None
			# "measured": testResultsDict.get('measured', None)
		}

		# logging.info("Results Dictionary: {}".format(self.resultsDict))

		# fileout = open('C:\\Documents and Settings\\npope\\Desktop\\out.txt', 'w')
		# fileout.write(json.dumps(self.rawData))
		# fileout.close()


def dataReturn(sess, resp):
	"""
	Callback function for async requests
	"""
	global requestCounter
	global totalRequest

	requestCounter += 1 # response from session request received

	logging.info("> Response from server6 recieved by localhost...")
	logging.info("> Received {} requests out of {} total".format(requestCounter, totalRequest))


def getTestResults(structure, checkedCalcsAndPropsDict):
	"""
	Gets pchemprop data from TEST ws.
	Inputs: chemical structure, dict of checked properties by calculator
	(e.g., { 'test': ['kow_no_ph', 'melting_point'] })
	Returns: dict of TEST props in template-friendly format (see pchemprop_tables)
	"""
	
	molID = 7 # NOTE: recycling id for now. this will change when db is implemented!!
	baseUrl = os.environ['CTS_TEST_SERVER']

	requests.get(baseUrl + "/test/test/calc/" + str(molID) + "/reset") # clear molecule values

	# give molecule an id to use for test calculations
	postData = { "id": molID, "smiles": str(structure) }
	requests.post(baseUrl + "/test/molecules", data=json.dumps(postData), 
								headers={'Content-Type': 'application/json'})

	session = FuturesSession() # start a sesh

	global totalRequest
	totalRequest = 0

	CalcDict = {
		'test': calcMap.TestCalc(), 
		'epi': calcMap.EpiCalc(), 
		'measured': calcMap.MeasuredCalc()
	}

	for calc, calcPropsList in checkedCalcsAndPropsDict.items():
		if calcPropsList and calc != 'chemaxon':
			Calc = CalcDict[calc] # select Calc object
			for prop in calcPropsList:
				try:
					for method in Calc.methods:
						url = baseUrl + Calc.getUrl(str(molID), prop, method)
						# session.get(url, timeout=30)
						# session.get(url, timeout=20, background_callback=dataReturn)
						totalRequest += 1
				except AttributeError:
					url = baseUrl + Calc.getUrl(str(molID), prop)
					# session.get(url, timeout=30)
					# session.get(url, timeout=20, background_callback=dataReturn)
					totalRequest += 1
				except requests.exceptions.Timeout:
					logging.warning("Timeout Exception! Call: {}->{}".format(calc, prop))
				except Exception as e:
					logging.warning("General Exception: {}".format(e))
				else:
					time.sleep(0.5) # maybe this will help TEST out some
					session.get(url, timeout=30)


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

		chemaxonDict = {} # dict of results (values) per method (keys)

		# TODO: Some segments of the below repeat and could probably be looped..
		# change that at some point
		for prop in chemaxonPropsList:
			if prop == "water_sol":
				postDict = {
					"chemical": structure,
					"solubility": {
						"pHLower": 0,
						"pHUpper": 14,
						"pHStep": 0.1,
						# "unit": "LOGS"
						"unit": "MGPERML"
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