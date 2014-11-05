"""
This is for laying the groundwork (and testing) 
for the CTS web service (http://pnnl.cloudapp.net)

2014-08-13 (np)
"""

import urllib2
import json
import requests
import pchemprop_parameters # Chemical Calculator and Transformation Pathway parameters
from REST import jchem_rest
from django.http import HttpRequest


baseUrl = 'http://pnnl.couldapp.net/efsws/rest/'

# From sip_model.py in ubertool_eco
# http_headers = {'Authorization' : 'Basic %s' % base64string, 'Content-Type' : 'application/json'}

http_headers = {'Content-Type' : 'application/json'}


class pchemprop(object):
	def __init__(self, run_type, chem_struct):

		self.run_type = run_type
		self.jid = jchem_rest.gen_jid() # get time of run
		self.chem_struct = chem_struct

		# chemical properties
		self.melting_point = melting_point
		self.boiling_point = boiling_point
		self.water_sol = water_sol
		self.vapor_press = vapor_press
		self.mol_diss = mol_diss
		self.ionization_con = ionization_con
		self.henrys_law_con = henrys_law_con
		self.kowNoPh = kowNoPh
		self.kowWph = kowWph
		self.kowPh = kowPh
		self.koc = koc

		# calcluators' checkboxes
		self.chemaxon = chemaxon
		self.epi = epi
		self.test = test
		self.sparc = sparc
		# self.measured = measured

		dataDict = {
						"melting_point":self.melting_point, 
						"boiling_point":self.boiling_point, 
						"water_sol":self.water_sol,
						"vapor_press":self.vapor_press, 
						"mol_diss":self.mol_diss, 
						"ionization_con":self.ionization_con,
						"henrys_law_con":self.henrys_law_con,
						"kowNoPh":self.kowNoPh,
						"kowWph": self.kowWph,
						"kowPh": self.kowPh,
						"koc":self.koc,
						"chemaxon": self.chemaxon,
						"epi": self.epi,
						"test": self.test,
						"sparc": self.sparc
					}

		# make request to calculators based on
		# checked calculator(s) and properties

		
		