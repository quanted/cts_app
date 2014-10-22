"""
This is for laying the groundwork (and testing) 
for the CTS web service (http://pnnl.cloudapp.net)

2014-08-13 (np)
"""

import urllib2
import json
import requests
import chemspec_parameters # Chemical Speciation parameters
# from REST import rest_funcs
from REST import jchem_rest
import logging
from django.http import HttpRequest 
import chemspec_tables


# Dict keys for chemical speciation parameters
pkaKeysOut = ['mostBasicPka', 'mostAcidicPka', 'parentImage', 'msImageUrlList', 'microDistData']
# pkaKeysIn = ["pKa_decimals", "pKa_pH_lower","pKa_pH_upper", "pKa_pH_increment", "pH_microspecies", "isoelectricPoint_pH_increment"]
# tautKeysOut = ['tautImageUrl']
# tautKeysIn = ["tautomer_maxNoOfStructures", "tautomer_pH"]
# stereoKeysOut = ['stereoImageUrl']
# stereoKeysIn = ["stereoisomers_maxNoOfStructures"]


class chemspec(object):
	def __init__(self, run_type, chem_struct, smiles, name, formula, mass, pkaChkbox, tautChkbox, stereoChkbox, pKa_decimals, pKa_pH_lower, pKa_pH_upper, pKa_pH_increment, pH_microspecies, 
			isoelectricPoint_pH_increment, tautomer_maxNoOfStructures, tautomer_pH, stereoisomers_maxNoOfStructures):

		self.jid = jchem_rest.gen_jid()

		self.run_type = run_type # hardcoded in pchemprop_output.py

		# Chemical Editor Tab
		self.chem_struct = chem_struct # SMILE of chemical on 'Chemical Editor' tab
		self.smiles = smiles
		self.name = name
		self.formula = formula
		self.mass = mass

		# Chemical Speciation Tab
		self.pKa_decimals = pKa_decimals
		self.pKa_pH_lower = pKa_pH_lower
		self.pKa_pH_upper = pKa_pH_upper
		self.pKa_pH_increment = pKa_pH_increment
		self.pH_microspecies = pH_microspecies
		self.isoelectricPoint_pH_increment = isoelectricPoint_pH_increment
		self.tautomer_maxNoOfStructures = tautomer_maxNoOfStructures
		self.tautomer_pH = tautomer_pH
		self.stereoisomers_maxNoOfStructures = stereoisomers_maxNoOfStructures

		dataDict = {"chem_struct":self.chem_struct}

		############# don't forget about pKa_decimal ###############

		if pkaChkbox == 'on':
			pkaInputsDict = {
				# "pKa_decimals":self.pKa_decimals, 
				"pKa_pH_lower":self.pKa_pH_lower,
				"pKa_pH_upper":self.pKa_pH_upper,
				"pKa_pH_increment":self.pKa_pH_increment,
				"pH_microspecies":self.pH_microspecies, 
				"isoelectricPoint_pH_increment":self.isoelectricPoint_pH_increment
			}
			dataDict.update(pkaInputsDict)
		
		if tautChkbox == 'on':
			tautInputsDict = {
				"tautomer_maxNoOfStructures":self.tautomer_maxNoOfStructures,
				"tautomer_pH":self.tautomer_pH
			}
			dataDict.update(tautInputsDict)

		if stereoChkbox == 'on':
			stereoInputsDict = {
				"stereoisomers_maxNoOfStructures":self.stereoisomers_maxNoOfStructures
			}
			dataDict.update(stereoInputsDict)

		request = HttpRequest()
		request.POST = dataDict
		results = jchem_rest.getChemSpecData(request) # gets json string response of chemical data

		output_val = json.loads(results.content) # convert json to dict

		fileout = open('C:\\Documents and Settings\\npope\\Desktop\\out.txt', 'w')
		fileout.write(json.dumps(output_val))
		fileout.close()

		self.pkaDict, self.stereoDict, self.tautDict = {}, {}, {}

		data_root = output_val['data'][0] #could have more than one in future (i.e., multiple chemical request)

		# Build results dictionaries
		if 'pKa' in data_root:
			self.pkaDict = getPkaInfo(output_val)
			# logging.warning("PKA IN ROOT")
		if 'stereoisomer' in data_root:
			self.stereoDict = getStereoInfo(output_val)
			# logging.warning("STEREO IN ROOT")
		if 'tautomerization' in data_root:
			self.tautDict = getTautInfo(output_val)
			# logging.warning("TAUT IN ROOT")

		# Get microspecies names and other info:
		

		for key, value in output_val.items():	
			logging.info(key, value)
			setattr(self, key, value)


# Builds pKa dictionary 
def getPkaInfo(output_val):

	pkaDict = {}

	# pkaKeys = ['mostBasicPka', 'mostAcidicPka', 'parentImage', 'msImageUrlList', 'microDistData']

	pkaDict = {key: None for key in pkaKeysOut} # Initialize dict values to None

	# Check if pka data exist
	if 'result' in output_val['data'][0]['pKa']:
		pkaDict.update({'mostBasicPka': output_val['data'][0]['pKa']['mostBasic']})
		pkaDict.update({'mostAcidicPka': output_val['data'][0]['pKa']['mostAcidic']})
		pkaDict.update({'parentImage': output_val['data'][0]['pKa']['result']['image']['imageUrl']})

		# Check if 'microspecies' key exist in dict
		if 'microspecies' in output_val['data'][0]['pKa']:
			# need to declare all the microspecies images:
			microspeciesList = output_val['data'][0]['pKa']['microspecies']

			msImageUrlList = [] # list of microspecies image urls
			for ms in microspeciesList:
				msImageUrlList.append(ms['image']['imageUrl'])

			pkaDict.update({'msImageUrlList': msImageUrlList})

			# get microspecies distribution data for plotting
			microDist = output_val['data'][0]['pKa']['chartData']

			microDistData = {}		
			for ms in microDist:
				valuesList = [] # format: [[ph1,con1], [ph2, con2], ...] per ms
				for vals in ms['values']:
					xy = [] # [ph1, con1]
					xy.append(vals['pH'])
					xy.append(vals['concentration'])
					valuesList.append(xy)

				microDistData.update({ms['key'] : valuesList})

			pkaDict.update({'microDistData': microDistData})

	logging.warning("PKA DICT: " + str(pkaDict))

	return pkaDict


def getStereoInfo(output_val):

	stereoDict = {'stereoImageUrl': [None]} # Initialize dict for stereoisomer image url

	stereoValues = output_val['data'][0]['stereoisomer']

	if 'result' in stereoValues:
		if 'image' in stereoValues['result']:
			stereoDict['stereoImageUrl'] = [stereoValues['result']['image']['imageUrl']]

	return stereoDict


def getTautInfo(output_val):

	tautDict = {'tautImageUrl': [None]}
	tautValues = output_val['data'][0]['tautomerization']

	if 'result' in tautValues:
		for taut in tautValues['result']:
			tautDict['tautImageUrl'] = [taut['image']['imageUrl']] #append to list

	return tautDict