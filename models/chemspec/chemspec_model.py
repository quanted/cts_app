"""
This is for laying the groundwork (and testing) 
for the CTS web service (http://pnnl.cloudapp.net)

2014-08-13 (np)
"""

import urllib2
import json
import requests
import chemspec_parameters # Chemical Speciation parameters
from REST import rest_funcs
from REST import jchem_rest
import logging
from django.http import HttpRequest


class chemspec(object):
	def __init__(self, run_type, chem_struct, pKa_decimals, pKa_pH_lower, pKa_pH_upper, pKa_pH_increment, pH_microspecies, 
			isoelectricPoint_pH_increment, tautomer_maxNoOfStructures, tautomer_maxNoOfStructures_pH, stereoisomers_maxNoOfStructures):

		self.jid = rest_funcs.gen_jid()

		self.run_type = run_type # hardcoded in pchemprop_output.py
		self.chem_struct = chem_struct # SMILE of chemical on 'Chemical Editor' tab
		self.pKa_decimals = pKa_decimals
		self.pKa_pH_lower = pKa_pH_lower
		self.pKa_pH_upper = pKa_pH_upper
		self.pKa_pH_increment = pKa_pH_increment
		self.pH_microspecies = pH_microspecies
		self.isoelectricPoint_pH_increment = isoelectricPoint_pH_increment
		self.tautomer_maxNoOfStructures = tautomer_maxNoOfStructures
		self.tautomer_maxNoOfStructures_pH = tautomer_maxNoOfStructures_pH
		self.stereoisomers_maxNoOfStructures = stereoisomers_maxNoOfStructures

		all_dic = {"chem_struct":self.chem_struct, "pKa_decimals":self.pKa_decimals, "pKa_pH_lower":self.pKa_pH_lower, "pKa_pH_upper":self.pKa_pH_upper,
					"pKa_pH_increment":self.pKa_pH_increment, "pH_microspecies":self.pH_microspecies, 
					"isoelectricPoint_pH_increment":self.isoelectricPoint_pH_increment, 
					"tautomer_maxNoOfStructures":self.tautomer_maxNoOfStructures,
					"tautomer_maxNoOfStructures_pH":self.tautomer_maxNoOfStructures_pH, 
					"stereoisomers_maxNoOfStructures":self.stereoisomers_maxNoOfStructures}

		micoDistPkaParams = {'pHLower':self.pKa_pH_lower, 'pHUpper':self.pKa_pH_upper, 'pHStep':self.pKa_pH_increment, 'temperature':298.0, 'micro':False, 'considerTautomerization':True, 'pKaLowerLimit':-10.0, 'pKaUpperLimit':20.0, 'prefix':'DYNAMIC'}
		microDistParams = {'pKa':micoDistPkaParams}
		structures = [{'structure':chem_struct}]
		include = ['pKa']
		microDistPayload = {'structures':structures, 'include':include, 'parameters': microDistParams}

		# fileout = open('C:\\Users\\nickpope\\Desktop\\testOut.txt', 'w')

		# fileout.write(str(microDistPayload))
		# fileout.write('\n')

		# jchem_rest.detailsBySmiles(self.chem_struct)

		# response = jchem_rest.getStructureDetails('pka', microDistPayload)

		# data = json.dumps(microDistPayload)

		request = HttpRequest()
		request.POST = microDistPayload

		response = jchem_rest.detailsBySmiles(request) 

		output_val = json.loads(response.content)

		
		# fileout.write(str(output_val))

		logging.warning(output_val)

		logging.info(output_val)

		logging.info(output_val.items())

		for key, value in output_val.items():
			logging.info(key, value)
			setattr(self, key, value)

#search for row id of structure:
# {
# 	"searchOptions": {
# 		"queryStructure": "CCCCCC",
# 		"dissimilarityThreshold": 0.5,
# 		"searchType": "SUBSTRUCTURE"
# 	},
# 	"display": {
# 		"include": ["cd_id"]
# 	}
# }


# microspecies distribution json
# {
#     "structures": [
#         {
#             "structure": "aspirin"
#         }
#     ],
#     "include": [
#         "pKa"
#     ],
#     "parameters": {
#         "pKa": {
#             "pHLower": 0,
#             "pHUpper": 14,
#             "pHStep": 0.1,
#             "temperature": 298,
#             "micro": false,
#             "considerTautomerization": true,
#             "pKaLowerLimit": -20,
#             "pKaUpperLimit": 10,
#             "prefix": "DYNAMIC"
#         }
#     }
# }