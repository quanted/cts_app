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

		# results = json.loads(results.content)
		# results = results.content

		self.results = results.content

		new_result = ''

		for char in self.results:
			if char == '"':
				char = '&quot;'
			new_result = new_result + char

		self.results = new_result

		logging.warning("TYPE " + str(type(self.results)))
		logging.warning("RESULTS " + str(self.results))
		# logging.warning("NEW RESULTS " + str(new_result))

		# for key, value in results.items():
		# 	logging.warning(key)
		# 	logging.warning(value)

		# logging.warning("type: " + str(type(results)))

		# self.results = '{'
		# for key, value in results.items():
		# 	self.results = self.results + str(key) + ': ' + str(value) + ', '
		# self.results = self.results + '}' 

		# logging.warning(type(self.results))

		# logging.warning("CONTENT: " + str(self.results))
        
		# output_val = json.loads(results.content)

		# logging.info(output_val)

		# logging.info(output_val.items())

		# for key, value in output_val.items():
		# 	logging.info(key, value)
		# 	setattr(self, key, value)

