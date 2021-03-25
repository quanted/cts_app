"""
2014-08-13 (np)
"""
import datetime
import json
import logging
import os
import requests
from ..generate_timestamp import gen_jid
from ..booleanize import booleanize
from ...cts_api import cts_rest



class chemspec(object):
	def __init__(self, run_type, chem_struct, smiles, orig_smiles, name, formula, cas, mass, exactMass, get_pka, get_taut,
				 get_stereo, pKa_decimals, pKa_pH_lower, pKa_pH_upper, pKa_pH_increment, pH_microspecies,
				 isoelectricPoint_pH_increment, tautomer_maxNoOfStructures, tautomer_pH, stereoisomers_maxNoOfStructures):

		self.title = "Calculate Chemical Speciation"
		self.jid = gen_jid()
		self.run_type = run_type

		# Chemical Editor Tab
		self.chem_struct = chem_struct  # SMILE of chemical on 'Chemical Editor' tab
		self.smiles = smiles
		self.orig_smiles = orig_smiles
		self.name = name
		self.formula = formula
		self.cas = cas
		self.mass = "{} g/mol".format(mass)
		self.exactMass = "{} g/mol".format(exactMass)

		# Checkboxes:
		self.get_pka = booleanize(get_pka)  # convert 'on'/'off' to bool
		self.get_taut = booleanize(get_taut)
		self.get_stereo = booleanize(get_stereo)

		# Chemical Speciation Tab
		self.pKa_decimals = None
		if pKa_decimals:
			self.pKa_decimals = int(pKa_decimals)
		self.pKa_pH_lower = pKa_pH_lower
		self.pKa_pH_upper = pKa_pH_upper
		self.pKa_pH_increment = pKa_pH_increment
		self.pH_microspecies = pH_microspecies
		self.isoelectricPoint_pH_increment = isoelectricPoint_pH_increment
		self.tautomer_maxNoOfStructures = tautomer_maxNoOfStructures
		self.tautomer_pH = tautomer_pH
		self.stereoisomers_maxNoOfStructures = stereoisomers_maxNoOfStructures

		# Output stuff:
		self.speciation_inputs = {}  # for batch mode use
		speciation_results = {}  # speciation prop results

		if self.run_type != 'batch':
			# Calls cts_rest to get speciation results:
			# speciation_url = os.environ.get('CTS_REST_SERVER') + "/cts/rest/speciation/run"
			post_data = self.__dict__  # payload is class attributes as dict
			# post_data['chemical'] = self.chem_struct  # cts rest uses 'chemical'
			post_data['chemical'] = self.smiles
			post_data['service'] = "getSpeciationData"
			post_data['run_type'] = "single"
			# speciation_results = requests.post(speciation_url,
			# 						data=json.dumps(post_data),
			# 						allow_redirects=True,
			# 						verify=False,
			# 						timeout=30)
			speciation_results = cts_rest.getChemicalSpeciationData(post_data)
			speciation_results = json.loads(speciation_results.content)

			if speciation_results.get('status'):
				speciation_results = speciation_results['data'].get('data')

		else:
			# Batch speciation calls are done through nodejs/socket.io
			# using cts_pchemprop_requests.html
			self.speciation_inputs = {
				'get_pka': True,
				'pKa_decimals': pKa_decimals,
				'pKa_pH_lower': pKa_pH_lower,
				'pKa_pH_upper': pKa_pH_upper,
				'pKa_pH_increment': pKa_pH_increment,
				'pH_microspecies': pH_microspecies,
				'isoelectricPoint_pH_increment': isoelectricPoint_pH_increment
			}
			self.speciation_inputs = self.speciation_inputs

		self.run_data = {
			'title': "Chemical Speciation Output",
			'run_type': self.run_type,
			'jid': self.jid,
			'time': datetime.datetime.strptime(self.jid, '%Y%m%d%H%M%S%f').strftime('%A, %Y-%B-%d %H:%M:%S'),
			'chem_struct': self.chem_struct,
			'smiles': self.smiles,
			'name': self.name,
			'formula': self.formula,
			'mass': self.mass,
			'exactMass': self.exactMass
		}

		self.run_data.update(speciation_results)