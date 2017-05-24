"""
2014-08-13 (np)
"""

# from cts_app.cts_calcs.chemaxon_cts import jchem_rest
# from cts_app.cts_api import cts_rest
import logging
from django.http import HttpRequest
# from cts_app.cts_calcs import data_walks
import datetime
import json

# from cts_app.cts_calcs.calculator import Calculator
from cts_app.cts_calcs.calculator_metabolizer import MetabolizerCalc


class gentrans(object):
    def __init__(self, run_type, chem_struct, smiles, orig_smiles, iupac, formula, mass,
                 exact_mass, abiotic_hydrolysis, abiotic_reduction, mamm_metabolism,
                 gen_limit, pop_limit, likely_limit):

        # self.jid = cts_rest.gen_jid()  # get time of run
        self.jid = MetabolizerCalc().gen_jid()
        self.run_type = run_type  # single or batch

        # Chemical Structure
        self.chem_struct = chem_struct  # chemical structure
        self.smiles = smiles
        self.orig_smiles = orig_smiles
        self.iupac = iupac
        self.formula = formula
        self.mass = '{} g/mol'.format(mass)
        self.exact_mass = '{} g/mol'.format(exact_mass)

        # Reaction Libraries
        self.abiotic_hydrolysis = abiotic_hydrolysis  # values: on or None
        self.abiotic_reduction = abiotic_reduction
        self.mamm_metabolism = mamm_metabolism

        self.gen_max = gen_limit
        self.gen_limit = gen_limit  # generation limit
        self.pop_limit = pop_limit  # population limit
        self.likely_limit = likely_limit

        # self.pchemprop_obj = pchemprop_obj # pchemprop object with inputs

        # Known keys for metabolizer on pnnl server (11-5-14)
        # metabolizerList = ["hydrolysis", "abiotic_reduction", "human_biotransformation"]
        metabolizerList = ["hydrolysis", "abiotic_reduction"]

        reactionLibs = {
            "hydrolysis": self.abiotic_hydrolysis,
            "abiotic_reduction": self.abiotic_reduction,
            # "human_biotransformation": self.mamm_metabolism
        }

        self.trans_libs = []
        for key, value in reactionLibs.items():
            if value:
                self.trans_libs.append(key)

        # NOTE: populationLimit is hard-coded to 0 as it currently does nothing

        self.metabolizer_request_post = {
            'structure': self.smiles,
            'generationLimit': self.gen_limit,
            'populationLimit': 0,
            # 'likelyLimit': self.likely_limit,
            'likelyLimit': 0.001,
            # 'transformationLibraries': self.trans_libs,
            'excludeCondition': ""  # 'generateImages': False
        }

        if len(self.trans_libs) > 0:
            self.metabolizer_request_post.update({'transformationLibraries': self.trans_libs})

        # if self.run_type != 'batch':
        #     try:
        #         # response = jchem_rest.getTransProducts(data_dict)
        #         response = MetabolizerCalc().getTransProducts(data_dict)
        #     except Exception as e:
        #         logging.warning("error making data request: {}".format(e))
        #         raise

        #     self.results = MetabolizerCalc().recursive(response, int(self.gen_limit), 'single')

        #     # Initializing here to fix ajax call script test_results being blank, triggering syntax error..
        #     self.test_results = []

        self.run_data = {
            'title': "Transformation Products Output",
            'jid': self.jid,
            'time': datetime.datetime.strptime(self.jid, '%Y%m%d%H%M%S%f').strftime('%A, %Y-%B-%d %H:%M:%S'),
            'chem_struct': self.chem_struct,
            'smiles': self.smiles,
            'iupac': self.iupac,
            'formula': self.formula,
            'mass': self.mass
        }