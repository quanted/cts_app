"""
2014-08-13 (np)
"""

from django.http import HttpRequest
import datetime
import json

from ...cts_calcs.calculator_metabolizer import MetabolizerCalc


class gentrans(object):
    def __init__(self, run_type, chem_struct, smiles, orig_smiles, name, formula, mass,
                 exactMass, cas, abiotic_hydrolysis, abiotic_reduction, mamm_metabolism, photolysis,
                 pfas_environmental, pfas_metabolism, gen_limit, pop_limit, likely_limit,
                 biotrans_metabolism, biotrans_libs, envipath_metabolism):

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
        self.photolysis = photolysis

        # Class-specific reaction libraries
        self.pfas_environmental  = pfas_environmental
        self.pfas_metabolism  = pfas_metabolism

        self.gen_max = int(gen_limit)
        self.gen_limit = int(gen_limit)  # generation limit
        self.pop_limit = pop_limit  # population limit
        self.likely_limit = likely_limit

        self.biotrans_metabolism = biotrans_metabolism
        self.biotrans_libs = biotrans_libs

        self.envipath_metabolism = envipath_metabolism

        reactionLibs = {
            "hydrolysis": self.abiotic_hydrolysis,
            "abiotic_reduction": self.abiotic_reduction,
            "photolysis": self.photolysis
        }

        self.trans_libs = []
        for key, value in reactionLibs.items():
            if value:
                self.trans_libs.append(key)

        if self.biotrans_metabolism:
            # self.trans_libs = ""
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
                'excludeCondition': "hasValenceError()"
            }
            if len(self.trans_libs) > 0:
                self.metabolizer_request_post.update({'transformationLibraries': self.trans_libs})

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