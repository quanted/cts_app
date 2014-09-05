"""
2014-08-13 (np)
"""

import urllib2
import json
import requests
import gentrans_parameters # Chemical Speciation parameters
from REST import rest_funcs
import logging

baseUrl = 'http://pnnl.cloudapp.net/efsws/rest/'

# From sip_model.py in ubertool_eco
# http_headers = {'Authorization' : 'Basic %s' % base64string, 'Content-Type' : 'application/json'}

headers = {'Content-Type' : 'application/json'}


class gentrans(object):
	def __init__(self, run_type, pKa_decimals, pKa_pH_lower, pKa_pH_upper, pKa_pH_increment, pH_microspecies, 
			isoelectricPoint_pH_increment, tautomer_maxNoOfStructures, tautomer_maxNoOfStructures_pH, stereoisomers_maxNoOfStructures):

		self.jid = rest_funcs.gen_jid()

		self.run_type = run_type # hardcoded in pchemprop_output.py
		self.pKa_decimals = pKa_decimals
		self.pKa_pH_lower = pKa_pH_lower
		self.pKa_pH_upper = pKa_pH_upper
		self.pKa_pH_increment = pKa_pH_increment
		self.pH_microspecies = pH_microspecies
		self.isoelectricPoint_pH_increment = isoelectricPoint_pH_increment
		self.tautomer_maxNoOfStructures = tautomer_maxNoOfStructures
		self.tautomer_maxNoOfStructures_pH = tautomer_maxNoOfStructures_pH
		self.stereoisomers_maxNoOfStructures = stereoisomers_maxNoOfStructures

		all_dic = {"pKa_decimals":self.pKa_decimals, "pKa_pH_lower":self.pKa_pH_lower, "pKa_pH_upper":self.pKa_pH_upper,
					"pKa_pH_increment":self.pKa_pH_increment, "pH_microspecies":self.pH_microspecies, 
					"isoelectricPoint_pH_increment":self.isoelectricPoint_pH_increment, 
					"tautomer_maxNoOfStructures":self.tautomer_maxNoOfStructures,
					"tautomer_maxNoOfStructures_pH":self.tautomer_maxNoOfStructures_pH, 
					"stereoisomers_maxNoOfStructures":self.stereoisomers_maxNoOfStructures}

		#data = json.dumps(all_dic)

		# url = baseUrl + 
		
		#self.jid = rest_funcs.gen_jid()
				
  #       url=os.environ['UBERTOOL_REST_SERVER'] + '/trex2/' + self.jid 
  #       response = requests.post(url, data=data, headers=http_headers, timeout=60)
  #       output_val = json.loads(response.content, cls=rest_funcs.NumPyDecoder)['result']
  #       output_val_uni=json.loads(output_val, cls=rest_funcs.NumPyDecoder)
  #       for key, value in output_val_uni.items():
  #           setattr(self, key, value)

		url = baseUrl + 'calculators/pka'

		parameters = {'basicLowerLimit':'-10.0', 'acidicUpperLimit':'20.0', 'pHLowerLimit':self.pKa_pH_lower, 'pHUpperLimit':self.pKa_pH_upper, 'temperature':'298.0'}

		#payload = {'parameters':{'basicLowerLimit':'-10.0', 'acidicUpperLimit':'20.0', 'pHLowerLimit':self.pKa_pH_lower, 'pHUpperLimit':self.pKa_pH_upper, 'temperature':'298.0'}, 'property':'pKa', 'provider':'chemaxon', 'substrate':''}
		payload = {'parameters':parameters, 'property':'pKa', 'provider':'chemaxon', 'substrate':'O=C1NN=C(N1)N(=O)=O'}

		data = json.dumps(payload)

  		#url = 'http://localhost:3443/Default.aspx'
        #payload = {'option':'nhdplus', 'huc':self.huc8, 'dt':Datatypes_for_NHDPlus_CHOICES}
        
		response = requests.post(url, data=data, headers=headers)
		logging.info(response.content)
        
		output_val = json.loads(response.content)['results']

		logging.info(output_val)

		logging.info(output_val.items())

		for key, value in output_val.items():
			logging.info(key, value)
			setattr(self, key, value)

