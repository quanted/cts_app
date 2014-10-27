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


# Dict keys for chemical speciation parameters (accessed in chemspec_tables.py)

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

		# fileout = open('C:\\Documents and Settings\\npope\\Desktop\\out.txt', 'w')
		# fileout.write(json.dumps(output_val))
		# fileout.close()

		self.pkaDict, self.stereoDict, self.tautDict, self.isoPtDict, self.majorMsDict = {}, {}, {}, {}, {}

		data_root = output_val['data'][0] #could have more than one in future (i.e., batch mode)

		# Build results dictionaries
		if 'pKa' in data_root:
			self.pkaDict = getPkaInfo(output_val)
		if 'isoelectricPoint' in data_root:
			self.isoPtDict = getIsoelectricPtInfo(output_val)
		if 'majorMicrospecies' in data_root:
			self.majorMsDict = getMajorMicrospecies(output_val)
		if 'stereoisomer' in data_root:
			self.stereoDict = getStereoInfo(output_val)
		if 'tautomerization' in data_root:
			self.tautDict = getTautInfo(output_val)

		# Get microspecies names and other info:
		

		for key, value in output_val.items():	
			logging.info(key, value)
			setattr(self, key, value)


# Builds isoelectricPoint dictionary
def getIsoelectricPtInfo(output_val):

	isoPtKeys = ['isoPt']

	isoPtDict = {}
	isoPtDict = {key: None for key in isoPtKeys} # initialize dict with None values

	isoPtData = output_val['data'][0]['isoelectricPoint']

	if isoPtData['hasIsoelectricPoint']:
		isoPtDict.update({'isoPt': isoPtData['isoelectricPoint']})

	if 'chartData' in isoPtData:
		isoPtList = isoPtData['chartData']['values'] # get list of xy values for isoPt

		valsList = []

		for pt in isoPtList:
			xyPair = []
			for key,value in pt.items():
				xyPair.append(value)
			valsList.append(xyPair)

		isoPtDict.update({'isoPtChartData': valsList})

	return isoPtDict


def getMajorMicrospecies(output_val):

	majorMsRoot = output_val['data'][0]['majorMicrospecies']
	majorMsDict = {}
	majorMsImage = '' # image path of structure

	if 'result' in majorMsRoot:

		# Get image data from result:
		if 'image' in majorMsRoot['result']:
			majorMsImage = majorMsRoot['result']['image']['imageUrl']
			majorMsDict.update({"image": majorMsRoot['result']['image']['imageUrl']})
		else:
			majorMsImage = 'No major microspecies'

		# Get structure data from result:
		structInfo = getStructInfo(majorMsRoot) # get info such as iupac, mass, etc.
		majorMsDict.update(structInfo)

	else:
		majorMsDict = None

	return majorMsDict


# Builds pKa dictionary 
def getPkaInfo(output_val):

	pkaDict = {}
	pkaKeys = ['mostBasicPka', 'mostAcidicPka', 'parentImage', 'msImageUrlList', 'microDistData']
	pkaDict = {key: None for key in pkaKeys} # Initialize dict values to None

	pkaRoot = output_val['data'][0]['pKa']

	# Check if pka data exist
	if 'result' in pkaRoot:
		pkaDict.update({'mostBasicPka': pkaRoot['mostBasic']})
		pkaDict.update({'mostAcidicPka': pkaRoot['mostAcidic']})

		# parentDict = {}
		# parentDict = getStructInfo

		pkaDict.update({'parentImage': pkaRoot['result']['image']['imageUrl']})

		# Check if 'microspecies' key exist in dict
		if 'microspecies' in pkaRoot:
			# need to declare all the microspecies images:
			microspeciesList = pkaRoot['microspecies']

			msImageUrlList = [] # list of microspecies image urls
			for ms in microspeciesList:

				# logging.warning("START STRUCTURE")
				# logging.warning(str(ms['structureData']['structure']))
				# logging.warning("END STRUCTURE")

				msStructDict = {} # list element in msImageUrlList
				msStructDict.update({"image": ms['image']['imageUrl']})
				structInfo = getStructInfo(ms['structureData']['structure'])
				msStructDict.update(structInfo)
				msImageUrlList.append(msStructDict)

			pkaDict.update({'msImageUrlList': msImageUrlList})

			# get microspecies distribution data for plotting
			microDist = pkaRoot['chartData']

			microDistData = []		
			for ms in microDist:
				valuesList = [] # format: [[ph1,con1], [ph2, con2], ...] per ms
				for vals in ms['values']:
					xy = [] # [ph1, con1]
					xy.append(vals['pH'])
					xy.append(vals['concentration'])
					valuesList.append(xy)

				# microDistData.update({ms['key'] : valuesList})
				microDistData.append(valuesList)

			pkaDict.update({'microDistData': microDistData})

	# logging.warning("PKA DICT: " + str(pkaDict))

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


"""
Appends structure info to image url 
Input: .mrv format structure
Output: dict with structure's info (i.e., formula, iupac, mass, smiles)
"""
def getStructInfo(mrvData):

	request = HttpRequest()
	request.POST = {"chemical": mrvData}

	response = jchem_rest.mrvToSmiles(request)

	structDict = json.loads(response.content)

	infoDict = {} # dict to be returned
	struct_root = {} # root of data in structInfo

	if 'data' in structDict:

		struct_root = structDict['data'][0]

		infoDict.update({"formula": struct_root['formula']})
		infoDict.update({"iupac":  struct_root['iupac']})
		infoDict.update({"mass":  struct_root['mass']})
		infoDict.update({"smiles":  struct_root['smiles']})

		return infoDict

	else:
		return None