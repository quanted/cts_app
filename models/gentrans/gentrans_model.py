"""
2014-08-13 (np)
"""

from chemaxon_cts import jchem_rest
import logging
from django.http import HttpRequest
import data_walks
from gentrans_parameters import gen_limit_max as gen_max
import datetime
from django.core.cache import cache
import json


class gentrans(object):
    def __init__(self, run_type, chem_struct, smiles, name, formula, mass,
                 abiotic_hydrolysis, abiotic_reduction, mamm_metabolism, gen_limit,
                 pop_limit, likely_limit):

        self.jid = jchem_rest.gen_jid()  # get time of run
        self.run_type = run_type  # single or batch

        # Chemical Structure
        self.chem_struct = chem_struct  # chemical structure
        self.smiles = smiles
        self.name = name
        self.formula = formula
        self.mass = '{} g/mol'.format(mass)

        # Reaction Libraries
        self.abiotic_hydrolysis = abiotic_hydrolysis  # values: on or None
        self.abiotic_reduction = abiotic_reduction
        self.mamm_metabolism = mamm_metabolism

        self.gen_max = gen_max
        self.gen_limit = gen_limit  # generation limit
        self.pop_limit = pop_limit  # population limit
        self.likely_limit = likely_limit

        # self.pchemprop_obj = pchemprop_obj # pchemprop object with inputs

        # Known keys for metabolizer on pnnl server (11-5-14)
        metabolizerList = ["hydrolysis", "abiotic_reduction", "human_biotransformation"]

        reactionLibs = {
            "hydrolysis": self.abiotic_hydrolysis,
            "abiotic_reduction": self.abiotic_reduction,
            "human_biotransformation": self.mamm_metabolism
        }

        self.trans_libs = []
        for key, value in reactionLibs.items():
            if value:
                self.trans_libs.append(key)

        # NOTE: populationLimit is hard-coded to 0 as it currently does nothing

        dataDict = {
            'structure': self.smiles,
            'generationLimit': self.gen_limit,
            'populationLimit': 0,
            # 'likelyLimit': self.likely_limit,
            'likelyLimit': 0.001,
            'transformationLibraries': self.trans_libs,
            'excludeCondition': ""  # 'generateImages': False
        }

        request = HttpRequest()
        request.POST = dataDict
        try:
            response = jchem_rest.getTransProducts(request)
        except Exception as e:
            logging.warning("error making data request: {}".format(e))
            raise

        # reformat data for outputting to tree structure:
        data_walks.j = 0
        data_walks.metID = 0
        self.results = data_walks.recursive(response.content)

        # Initializing here to fix ajax call script test_results being blank, triggering syntax error..
        self.test_results = []

        self.rawData = response.content

        # ++++ NEW STUFF FOR CSV DOWNLOADS, USES DJANGO CACHING ++++++++++++++
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