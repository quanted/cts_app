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

baseUrl = 'http://pnnl.cloudapp.net/efsws/rest/'

# From sip_model.py in ubertool_eco
# http_headers = {'Authorization' : 'Basic %s' % base64string, 'Content-Type' : 'application/json'}

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
		# self.results = """
	 #    {
	 #        "id": "SMILES1",
	 #        "name": "SMILES1",
	 #        "data": {},
	 #        "children": [{
	 #            "id": "SMILES2a",
	 #            "name": "SMILES2a",
	 #            "data": {},
	 #            "children": [{
	 #                "id": "SMILES3a",
	 #                "name": "SMILES3a",
	 #                "data": {},
	 #                "children": []
	 #            }]
	 #        }, {
	 #            "id": "SMILES2b",
	 #            "name": "SMILES2b",
	 #            "data": {},
	 #            "children": []
	 #        }, {
	 #            "id": "SMILES2c",
	 #            "name": "SMILES2c",
	 #            "data": {},
	 #            "children": []
	 #        }]
	 #    }
	 #    """


		# fileout = open('C:\\Documents and Settings\\npope\\Desktop\\out.txt', 'w')
		# fileout.write(results.content)
		# fileout.close()

		# new_result = ''

		# for char in self.results:
		# 	if char == '"':
		# 		char = '&quot;'
		# 	new_result = new_result + char

		# self.results = new_result

		self.results = parseJsonForJit(self.results)

		# self.results = 

		
		# output_val = json.loads(results.content)

		# logging.info(output_val)

		# logging.info(output_val.items())

		# for key, value in output_val.items():
		# 	logging.info(key, value)
		# 	setattr(self, key, value)


"""
This is a "hacked" way to transform the keys
in the resultant json string into the ones
used by jit.js. It just reads through the json
string and replaces certain keys (e.g., smiles)
with the jit.js keys (e.g., name).
This bypasses any need of recursive statements (for now)
"""
def parseJsonForJit(jsonStr):
	# index = jsonStr.find("smiles")
	jsonStr = jsonStr.replace("smiles", "name")
	# logging.warning(jsonStr)

	fileout = open('C:\\Documents and Settings\\npope\\Desktop\\out.txt', 'w')
	fileout.write(jsonStr)
	fileout.close()

	return jsonStr


# def insert_dash(string, index):
#     return string[:index] + '"name": ' + string[index:]


def parseJsonForJit1(jsonStr, genPop):
	"""
	Need to reformat json to:
	{
		id: "id"
		name: "name"
		data: {}
		children: [{}]
	}
	where children continues the tree
	"""

	logging.warning("GEN POP " + str(genPop))

	jsonDict = json.loads(jsonStr)

	root = jsonDict['results']
	parent = root.keys()[0] # parent species
	mainList = [parent] 

	jitDict = {
		"id": parent,
		"name": parent,
		"data": {},
		"children": []
	}

	n = int(genPop) # number of generations of metabolites
	relRoot = root[parent]['metabolites'] # initialize relative root
	y = len(relRoot) # number of 1st gen metabolites
	logging.warning(y)
	recursion_loop(len(relRoot), n, mainList, relRoot)

	# loop through each generation of metabolites
	# for i in range(n):

	# 	genList = [] # list per generation (to append to mainList)

	# 	# loop through metabolites in generation
	# 	for key in relRoot.keys():
	# 		logging.warning("META KEY " + key)
	# 		genList.append[key]

	# 	mainList.append(genList)
	# 	# still have to "walk" through dict

	# logging.warning(str(jitDict))

	# fileout = open('C:\\Documents and Settings\\npope\\Desktop\\out.txt', 'w')
	# fileout.write(json.dumps(jitDict))
	# fileout.close()

	return None


"""
Recursive loop for metabolites
y - number of metabolites per generation
n - number of generations
mainList - list to append SMILES to (e.g., [parent, gen1List, gen2List, ...])
"""
def recursion_loop(y, n, mainList, relRoot):

	if n >= 1:
		logging.warning("above loop")
		for i in range(y):
			genList = []
			genList.append(relRoot.keys()[i]) # append key (SMILES) to genList
			logging.warning("in loop: " + str(genList))
			# relRoot = relRoot[key]['metabolites']
			recursion_loop(y, n - 1, genList, relRoot)
	# else:
	# 	# whatever()
	# 	stuff = 1
	return None

