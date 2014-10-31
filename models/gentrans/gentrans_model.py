"""
2014-08-13 (np)
"""

import urllib2
import json
import requests
import gentrans_parameters # Chemical Speciation parameters
# from REST import rest_funcs
from REST import jchem_rest
import logging
from django.http import HttpRequest
import data_walks 

baseUrl = 'http://pnnl.cloudapp.net/efsws/rest/'

headers = {'Content-Type' : 'application/json'}


class gentrans(object):
	def __init__(self, run_type, chem_struct, abiotic_hydrolysis, abiotic_reduction, gen_limit, pop_limit, likely_limit):

		# self.jid = rest_funcs.gen_jid()
		self.jid = jchem_rest.gen_jid()

		self.run_type = run_type
		self.chem_struct = chem_struct
		self.abiotic_hydrolysis = abiotic_hydrolysis
		self.abiotic_reduction = abiotic_reduction
		self.gen_limit = gen_limit
		self.pop_limit = pop_limit
		self.likely_limit = likely_limit

		self.trans_libs = ["hydrolysis","abiotic_reduction"]

		logging.warning("GEN LIMIT: " + self.gen_limit)
		logging.warning("CHEM: " + self.chem_struct)



		#########################################
		self.gen_limit = 3
		#######################################


		dataDict = {
					'structure': self.chem_struct,
					'generationLimit': self.gen_limit,
					'populationLimit': self.pop_limit,
					'likelyLimit': self.likely_limit,
					'transformationLibraries': self.trans_libs,
					'excludeCondition': "",
					'generateImages': True
					}

		logging.warning("DATA DICT: " + dataDict['structure'])

		request = HttpRequest()
		request.POST = dataDict
		results = jchem_rest.getTransProducts(request)

		self.results = results.content

		logging.warning("parsing results...")

		# reformat data for outputting to tree structure:
		data_walks.metID = 0
		self.results = data_walks.recursive(self.results)

		# fileout = open('C:\\Documents and Settings\\npope\\Desktop\\out.txt', 'w')
		# fileout.write(self.results)
		# fileout.close()

		logging.warning("end parsing...")		


# def parseJsonForJit(jsonStr):
# 	jsonDict = json.loads(jsonStr)
# 	root = jsonDict['results']

# 	reDict = {}
# 	parent = root.keys()[0]
# 	reDict.update({"id": metID, "name": parent, "data": {}, "children": []})
# 	root = root[parent]['metabolites']
# 	reDict.update(recurse(root))

# 	return json.dumps(reDict)


# # metID = 0 # unique id for each node
# # logging.warning("metID: " + str(metID))

# ##### WORKING VERSION ASIDE FROM metID recompile issue ######
# def recurse(root):
# 	global metID
# 	metID += 1
# 	newDict ={}

# 	logging.warning(root.keys())

# 	if metID == 1:
# 		parent = root.keys()[0]
# 		newDict.update({"id": metID, "name": parent, "data": {}, "children": []})
# 		root = root[parent]
# 	else:
# 		newDict.update({"id": metID, "name": root['smiles'], "data": {}, "children": []})
# 		newDict['data'].update({"degradation": root['degradation']})

# 	for key, value in root.items():
# 		if isinstance(value, dict):
# 			for key2, value2 in root[key].items():
# 				root2 = root[key][key2]
# 				if len(root2) > 0: 
# 					newDict['children'].append(recurse(root2))

# 	return newDict
# #################################################################