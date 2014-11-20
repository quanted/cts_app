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


class pchemprop(object):
	def __init__(self, run_type, chem_struct, chemaxon, epi, test, sparc, measured, 
					melting_point, boiling_point, water_sol, vapor_press, mol_diss, 
					ion_con, henrys_law_con, kowNoPh, kowWph, kowPh, koc):

		self.run_type = run_type # defaults to "single", "batch" coming soon...
		self.jid = jchem_rest.gen_jid() # get time of run
		self.chem_struct = chem_struct

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

		checkedPropsDict = {
			"melting_point": self.melting_point,
			"boiling_point": self.boiling_point,
			"water_sol": self.water_sol,
			"vapor_press": self.vapor_press,
			"mol_diss": self.mol_diss,
			"ion_con": self.ion_con,
			"henrys_law_con": self.henrys_law_con,
			"kowNoPh": self.kowNoPh,
			"kowWph": self.kowWph,
			"kowPh": self.kowPh,
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
		dataDict = {}

		for calcKey, calcValue in calcluatorsDict.items():
			if calcValue == 'true':
				# get checked parameters that are available for calculator
				propList = []
				for propKey, propValue in checkedPropsDict.items():
					# find checked properties
					if propValue == 'on':
						# check if property is available for calculator:
						if pchemprop_parameters.pchempropAvailable(calcKey, propKey):
							propList.append(propKey)
				dataDict.update({calcKey:propList})

		logging.warning(dataDict)

		# For chemaxon:
		# if ion_con is requested, get pKa values
		# if kowNoPh is requested, get logP values
		# if kowWph is requested, get logD values with pH value: kowPh

		# NOTE: separate above loop for dataDict from calls so one request
		# can be used for multiple properties. I think this can be done using
		# chemicalTerms()

		# loop through checked calculators and their available, checked properties
		# make those calls
		for key, value in dataDict.items():
			if key == "chemaxon":
				for prop in value:
					# loop through props in list
					if prop == "ion_con":
						# make call to getChemSpecData() for pKa values
						postDict = {
							"chem_struct": self.chem_struct,
							"pKa": { 
								"pHLower":0, # note: default values
								"pHUpper":14,
								"pHStep":0.1
							}
						}
						request = HttpRequest()
						request.POST = postDict
						response = jchem_rest.getChemSpecData(request)
						self.rawData = response.content


		# dataDict = {
		# 				"melting_point":self.melting_point, 
		# 				"boiling_point":self.boiling_point, 
		# 				"water_sol":self.water_sol,
		# 				"vapor_press":self.vapor_press, 
		# 				"mol_diss":self.mol_diss, 
		# 				"ion_con":self.ion_con,
		# 				"henrys_law_con":self.henrys_law_con,
		# 				"kowNoPh":self.kowNoPh,
		# 				"kowWph": self.kowWph,
		# 				"kowPh": self.kowPh,
		# 				"koc":self.koc,
		# 				"chemaxon": self.chemaxon,
		# 				"epi": self.epi,
		# 				"test": self.test,
		# 				"sparc": self.sparc,
		# 				"measured": self.measured
		# 			}

		# Check available properties for checked calculators
		# NOTE: calculator checkboxes are coming back as 'True' or 


		# checks prop availability for calculator:
		# pchemprop_parameters.pchemCalcFilter(calculator, prop)

		
		