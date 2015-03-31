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

from REST.calculator_map import Calculator as calc
from REST.jchem_rest import JchemProperty as jp
from requests_futures.sessions import FuturesSession


n = 3 # number of decimal places to round values
# requestCounter = 0 # yeah figure out a better way to do this...
# totalRequest = 0 # total number of request. again, better way please


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


		if 'chemaxon' in self.checkedCalcsAndPropsDict:
			self.chemaxonResultsDict = newGetChemaxonResults(self.chem_struct, self.checkedCalcsAndPropsDict, 
																self.kow_ph)


def newGetChemaxonResults(structure, checkedCalcsAndPropsDict, phForLogD):
	chemaxonPropsList = checkedCalcsAndPropsDict.get('chemaxon', None)
	logging.info("PH TYPE: {}".format(type(phForLogD)))
	if chemaxonPropsList:
		calcObj = calc.getCalcObject('chemaxon') # get instance of chemaxon calculator
		chemaxonResults = {}
		for prop in chemaxonPropsList:
			if prop == 'water_sol':
				propObj = jp.getPropObject('solubility')
				propObj.makeDataRequest(structure)
				chemaxonResults.update({prop: propObj.getSolubility()})
			elif prop == 'ion_con':
				propObj = jp.getPropObject('pKa')
				propObj.makeDataRequest(structure)
				chemaxonResults.update({prop: {'pKa': propObj.getMostAcidicPka(), 'pKb': propObj.getMostBasicPka()}})
			elif prop == 'kow_no_ph':
				propObj = jp.getPropObject('logP')
				propObj.makeDataRequest(structure)
				chemaxonResults.update({prop: propObj.getLogP()})
			elif prop == 'kow_wph':
				propObj = jp.getPropObject('logD')
				propObj.makeDataRequest(structure)
				chemaxonResults.update({prop: propObj.getLogD(phForLogD)})
		return chemaxonResults
	else:
		return None