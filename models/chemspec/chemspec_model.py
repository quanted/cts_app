"""
2014-08-13 (np)
"""

import json
# from chemaxon_cts import jchem_rest
# from chemaxon_cts.jchem_calculator import ChemaxonCalc
# from cts_app.cts_calcs.chemaxon_cts.jchem_calculator import ChemaxonCalc
from cts_app.cts_calcs.calculator_chemaxon import ChemaxonCalc
import logging
import datetime
# from REST import cts_rest
from cts_app.cts_api import cts_rest


class chemspec(object):
	def __init__(self, run_type, chem_struct, smiles, orig_smiles, name, formula, mass, exactMass, get_pka, get_taut,
				 get_stereo, pKa_decimals, pKa_pH_lower, pKa_pH_upper, pKa_pH_increment, pH_microspecies,
				 isoelectricPoint_pH_increment, tautomer_maxNoOfStructures, tautomer_pH, stereoisomers_maxNoOfStructures):


		logging.warning("INSIDE CHEMSPEC MODEL NOW..")

		self.jid = cts_rest.gen_jid()  # timestamp

		self.run_type = run_type

		# Chemical Editor Tab
		self.chem_struct = chem_struct  # SMILE of chemical on 'Chemical Editor' tab
		self.smiles = smiles
		self.orig_smiles = orig_smiles
		self.name = name
		self.formula = formula

		logging.warning("BEFORE MASS DECLARATION")

		self.mass = "{} g/mol".format(mass)
		self.exactMass = "{} g/mol".format(exactMass)

		logging.warning("AFTER MASS DECLARATION")

		# Checkboxes:
		jchem_prop = ChemaxonCalc()
		self.get_pka = jchem_prop.booleanize(get_pka)  # convert 'on'/'off' to bool
		self.get_taut = jchem_prop.booleanize(get_taut)
		self.get_stereo = jchem_prop.booleanize(get_stereo)

		logging.warning("AFTER BOOL STUFF")


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
		self.jchemPropObjects = {}
		self.jchemDictResults = {}
		self.speciation_inputs = {}  # for batch mode use


		pkaObj, majorMsObj, isoPtObj, tautObj, stereoObj = None, None, None, None, None


		logging.warning("AFTER INITIALIZING EVERYTHING")
		logging.warning("run_type: {}".format(self.run_type))

		if self.run_type != 'batch':

			logging.warning("Making calls inside chemspec model, single mode...")

			if self.get_pka:

				logging.warning("self.get_pka: {}".format(self.get_pka))

				# make call for pKa:
				pkaObj = ChemaxonCalc.getPropObject('pKa')
				jchem_prop.setPostDataValues({
					"pHLower": self.pKa_pH_lower,
					"pHUpper": self.pKa_pH_upper,
					"pHStep": self.pKa_pH_increment,
				})
				logging.warning("Calling request handler")
				jchem_prop.make_data_request(self.smiles, pkaObj)

				# make call for majorMS:
				majorMsObj = ChemaxonCalc.getPropObject('majorMicrospecies')
				jchem_prop.setPostDataValue('pH', self.pH_microspecies)
				jchem_prop.make_data_request(self.smiles, majorMsObj)

				# make call for isoPt:
				isoPtObj = ChemaxonCalc.getPropObject('isoelectricPoint')
				jchem_prop.setPostDataValue('pHStep', self.isoelectricPoint_pH_increment)
				jchem_prop.make_data_request(self.smiles, isoPtObj)

			if self.get_taut:

				logging.warning("self.get_taut: {}".format(self.get_taut))

				tautObj = ChemaxonCalc.getPropObject('tautomerization')
				jchem_prop.setPostDataValues({
					"maxStructureCount": self.tautomer_maxNoOfStructures,
					"pH": self.tautomer_pH,
					"considerPH": True
				})
				jchem_prop.make_data_request(self.smiles, tautObj)

			if self.get_stereo:

				logging.warning("self.get_stereo: {}".format(self.get_stereo))

				# TODO: set values for max stereos!!!
				stereoObj = ChemaxonCalc.getPropObject('stereoisomer')
				jchem_prop.setPostDataValue('maxStructureCount', self.stereoisomers_maxNoOfStructures)
				jchem_prop.make_data_request(self.smiles, stereoObj)

			self.jchemPropObjects = {
				'pKa': pkaObj,
				'majorMicrospecies': majorMsObj,
				'isoelectricPoint': isoPtObj,
				'tautomerization': tautObj,
				'stereoisomers': stereoObj
			}

		else:

			# for batch mode, get inputs but don't get
			# data until output page loads. this is because batch
			# speciation calls are done through nodejs/socket.io
			# using cts_pchemprop_requests.html

			logging.warning("INSIDE CHEMSPEC MODEL BATCH CONDITION..")

			self.speciation_inputs = {
				'pKa_decimals': pKa_decimals,
				'pKa_pH_lower': pKa_pH_lower,
				'pKa_pH_upper': pKa_pH_upper,
				'pKa_pH_increment': pKa_pH_increment,
				'pH_microspecies': pH_microspecies,
				'isoelectricPoint_pH_increment': isoelectricPoint_pH_increment
			}
			self.speciation_inputs = json.dumps(self.speciation_inputs)

		self.run_data = {
			'title': "Chemical Speciation Output",
			'jid': self.jid,
			'time': datetime.datetime.strptime(self.jid, '%Y%m%d%H%M%S%f').strftime('%A, %Y-%B-%d %H:%M:%S'),
			'chem_struct': self.chem_struct,
			'smiles': self.smiles,
			'name': self.name,
			'formula': self.formula,
			'mass': self.mass,
			'exactMass': self.exactMass
		}

		speciation_results = jchem_prop.getSpeciationResults(self.jchemPropObjects)
		self.run_data.update(speciation_results)