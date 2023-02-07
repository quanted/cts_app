"""
2014-08-13 (np)
"""

from django.http import HttpRequest
import datetime
import json

from ...cts_calcs.calculator_metabolizer import MetabolizerCalc


class gentrans(object):
	def __init__(self, run_type, chem_struct, smiles, orig_smiles, name, formula, mass,
				 exactMass, cas, abiotic_hydrolysis, abiotic_reduction, mamm_metabolism, photolysis_unranked,
				 photolysis_ranked, pfas_environmental, pfas_metabolism, gen_limit, pop_limit,
				 likely_limit, biotrans_metabolism, biotrans_libs, envipath_metabolism, include_rates, tree_type):

		self.title = "Generate Transformation Products"
		self.jid = MetabolizerCalc().gen_jid()
		self.run_type = run_type  # single or batch

		# Chemical Structure
		self.chem_struct = chem_struct  # chemical structure
		self.smiles = smiles
		self.orig_smiles = orig_smiles
		# self.iupac = iupac
		self.name = name

		self.formula = formula
		self.mass = '{} g/mol'.format(mass)
		self.exactMass = '{} g/mol'.format(exactMass)
		self.cas = cas

		self.calc = "metabolizer"

		# Reaction Libraries
		self.abiotic_hydrolysis = abiotic_hydrolysis  # values: on or None
		self.abiotic_reduction = abiotic_reduction
		self.mamm_metabolism = mamm_metabolism
		self.photolysis_unranked = photolysis_unranked
		self.photolysis_ranked = photolysis_ranked

		# Chemical class-specific reaction libraries
		self.pfas_environmental  = pfas_environmental
		self.pfas_metabolism  = pfas_metabolism

		self.gen_max = int(gen_limit)
		self.gen_limit = int(gen_limit)  # generation limit
		self.pop_limit = pop_limit  # population limit
		self.likely_limit = likely_limit

		self.biotrans_metabolism = biotrans_metabolism
		self.biotrans_libs = biotrans_libs

		self.envipath_metabolism = envipath_metabolism

		self.include_rates = include_rates

		self.tree_type = tree_type

		reactionLibs = {
			"hydrolysis": self.abiotic_hydrolysis,
			"abiotic_reduction": self.abiotic_reduction,
			"photolysis_unranked": self.photolysis_unranked,
			"photolysis_ranked": self.photolysis_ranked,
			"mammalian_metabolism": self.mamm_metabolism,
			"pfas_environmental": self.pfas_environmental,
			"pfas_metabolism": self.pfas_metabolism
		}

		self.trans_libs = []

		if self.abiotic_hydrolysis and (self.photolysis_ranked or self.photolysis_unranked):
			self.trans_libs.append("combined_photolysis_abiotic_hydrolysis")
		elif self.abiotic_hydrolysis and self.abiotic_reduction:
			self.trans_libs.append("combined_abioticreduction_hydrolysis")
		else:        
			for key, value in reactionLibs.items():
				if value:
					self.trans_libs.append(key)

		if self.biotrans_metabolism:
			self.calc = "biotrans"
			self.metabolizer_request_post = {
				'chemical': self.smiles,
				'gen_limit': self.gen_limit,
				'prop': self.biotrans_libs
			}
		elif self.envipath_metabolism:
			self.calc = "envipath"
			self.metabolizer_request_post = {
				'chemical': self.smiles,
				'gen_limit': self.gen_limit
			}
		else:
			self.metabolizer_request_post = {
				'structure': self.smiles,
				'generationLimit': self.gen_limit,
				'populationLimit': 0,
				'likelyLimit': 0.1,
				'excludeCondition': "hasValenceError()",
				'transformationLibraries': self.trans_libs
			}
			if len(self.trans_libs) > 0:
				self.metabolizer_request_post.update({'transformationLibraries': self.trans_libs})

			if self.tree_type == "simplified_tree":
				# Simplified tree selected, sets 'unique_metabolites' key to true:
				self.metabolizer_request_post.update({"unique_metabolites": True})
			else:
				self.metabolizer_request_post.update({"unique_metabolites": False})

		self.run_data = {
			'title': "Transformation Products Output",
			'jid': self.jid,
			'time': datetime.datetime.strptime(self.jid, '%Y%m%d%H%M%S%f').strftime('%A, %Y-%B-%d %H:%M:%S'),
			'chem_struct': self.chem_struct,
			'smiles': self.smiles,
			'name': self.name,
			'formula': self.formula,
			'mass': self.mass
		}