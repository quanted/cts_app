"""
This is for laying the groundwork (and testing) 
for the CTS web service (http://pnnl.cloudapp.net)

2014-08-13 (np)
"""

import urllib2
import json
import requests
import pchemprop_parameters # Chemical Calculator and Transformation Pathway parameters
import chemspec_parameters # Chemical Speciation parameters

baseUrl = 'http://pnnl.couldapp.net/efsws/rest/'

# From sip_model.py in ubertool_eco
# http_headers = {'Authorization' : 'Basic %s' % base64string, 'Content-Type' : 'application/json'}

http_headers = {'Content-Type' : 'application/json'}


class pchemprop(object):
	def __init__(self, run_type, pKa_decimals, pKa_pH_lower, pKa_pH_upper, pKa_pH_increment, pH_microspecies, 
			isoelectricPoint_pH_increment, tautomer_maxNoOfStructures, tautomer_maxNoOfStructures_pH, stereoisomers_maxNoOfStructures,
			melting_point, boiling_point, water_sol, vapor_press, mol_diss, ionization_con, henrys_law_con, kow, koc, dist_coeff,
			reactionSys_CHOICES, reactionSys, respiration_CHOICES, respiration):

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
		self.melting_point = melting_point
		self.boiling_point = boiling_point
		self.water_sol = water_sol
		self.vapor_press = vapor_press
		self.mol_diss = mol_diss
		self.ionization_con = ionization_con
		self.henrys_law_con = henrys_law_con
		self.kow = kow
		self.koc = koc
		self.dist_coeff = dist_coeff
		self.reactionSys_CHOICES = reactionSys_CHOICES
		self.reactionSys = reactionSys
		self.respiration_CHOICES = respiration_CHOICES
		self.respiration = respiration

		all_dic = {"pKa_decimals":self.pKa_decimals, "pKa_pH_lower":self.pKa_pH_lower, "pKa_pH_upper":self.pKa_pH_upper,
					"pKa_pH_increment":self.pKa_pH_increment, "pH_microspecies":self.pH_microspecies, 
					"isoelectricPoint_pH_increment":self.isoelectricPoint_pH_increment, "tautomer_maxNoOfStructures":self.tautomer_maxNoOfStructures,
					"tautomer_maxNoOfStructures_pH":self.tautomer_maxNoOfStructures_pH, "stereoisomers_maxNoOfStructures":self.stereoisomers_maxNoOfStructures,
					"melting_point":self.melting_point, "boiling_point":self.boiling_point, "water_sol":self.water_sol,
					"vapor_press":self.vapor_press, "mol_diss":self.mol_diss, "ionization_con":self.ionization_con,
					"henrys_law_con":self.henrys_law_con, "kow":self.kow, "koc":self.koc, "dist_coeff":self.dist_coeff,
					"reactionSys_CHOICES":self.reactionSys_CHOICES, "reactionSys":self.reactionSys, 
					"respiration_CHOICES":self.respiration_CHOICES, "respiration":self.respiration}

		data = json.dumps(all_dic)

		url = baseUrl + 


  #       data = json.dumps(all_dic)

  #       self.jid = rest_funcs.gen_jid()
  #       url=os.environ['UBERTOOL_REST_SERVER'] + '/trex2/' + self.jid 
  #       response = requests.post(url, data=data, headers=http_headers, timeout=60)
  #       output_val = json.loads(response.content, cls=rest_funcs.NumPyDecoder)['result']
  #       output_val_uni=json.loads(output_val, cls=rest_funcs.NumPyDecoder)
  #       for key, value in output_val_uni.items():
  #           setattr(self, key, value)

