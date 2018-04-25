"""
2014-08-13 (np)
"""
import datetime

from . import pchemprop_parameters  # Chemical Calculator and Transformation Pathway parameters
from ...cts_calcs.calculator import Calculator

n = 2  # number of decimal places to round values


class PChemProp(object):
    def __init__(self, run_type, chem_struct=None, smiles=None, name=None, formula=None, exactMass=None, mass=None,
                 cas=None, chemaxon=None, epi=None, test=None, sparc=None, measured=None, melting_point=None,
                 boiling_point=None, water_sol=None, water_sol_ph=None, vapor_press=None, mol_diss=None, mol_diss_air=None,
                 ion_con=None, henrys_law_con=None, kow_no_ph=None, kow_wph=None, kow_ph=None, koc=None, log_bcf=None, log_baf=None):
        
        self.run_type = run_type  # defaults to "single", "batch" coming soon...
        self.title = "Calculate Physicochemical Properties"
        self.jid = Calculator().gen_jid()

        # chemical structure
        self.chem_struct = chem_struct
        self.smiles = smiles
        self.name = name
        self.formula = formula
        # make sure to include units when assigning mass - 'g/mol'
        self.exactMass = "{} g/mol".format(exactMass)
        self.mass = "{} g/mol".format(mass)
        self.cas = cas

        # chemical properties (values 'on' or None) -- django params
        self.melting_point = melting_point
        self.boiling_point = boiling_point
        self.water_sol = water_sol
        self.water_sol_ph = water_sol_ph
        self.vapor_press = vapor_press
        self.mol_diss = mol_diss
        self.mol_diss_air = mol_diss_air
        self.ion_con = ion_con
        self.henrys_law_con = henrys_law_con
        self.kow_no_ph = kow_no_ph
        self.kow_wph = kow_wph
        self.kow_ph = kow_ph
        self.koc = koc
        self.log_bcf = log_bcf
        self.log_baf = log_baf

        self.chemaxon = chemaxon
        self.sparc = sparc
        self.epi = epi
        self.test = test
        self.measured = measured

        self.checkedPropsDict = {}
        self.calcluatorsDict = {}

        # Property checkboxes' values:
        self.checkedPropsDict = {
            "melting_point": self.melting_point,
            "boiling_point": self.boiling_point,
            "water_sol": self.water_sol,
            "water_sol_ph": self.water_sol_ph,
            "vapor_press": self.vapor_press,
            "mol_diss": self.mol_diss,
            "mol_diss_air": self.mol_diss_air,
            "ion_con": self.ion_con,
            "henrys_law_con": self.henrys_law_con,
            "kow_no_ph": self.kow_no_ph,
            "kow_wph": self.kow_wph,
            "kow_ph": self.kow_ph,
            "koc": self.koc,
            "log_bcf": self.log_bcf,
            "log_baf": self.log_baf
        }
        # calculator checkboxes' values:
        self.calcluatorsDict = {
            "chemaxon": self.chemaxon,
            "epi": self.epi,
            "test": self.test,
            "sparc": self.sparc,
            "measured": self.measured
        }

    def fillCalcsandPropsDict(self):

        self.checkedPropsDict = {
            "melting_point": self.melting_point,
            "boiling_point": self.boiling_point,
            "water_sol": self.water_sol,
            "water_sol_ph": self.water_sol_ph,
            "vapor_press": self.vapor_press,
            "mol_diss": self.mol_diss,
            "mol_diss_air": self.mol_diss_air,
            "ion_con": self.ion_con,
            "henrys_law_con": self.henrys_law_con,
            "kow_no_ph": self.kow_no_ph,
            "kow_wph": self.kow_wph,
            "kow_ph": self.kow_ph,
            "koc": self.koc,
            "log_bcf": self.log_bcf,
            "log_baf": self.log_baf
        }

        # calculator checkboxes' values:
        self.calcluatorsDict = {
            "chemaxon": self.chemaxon,
            "epi": self.epi,
            "test": self.test,
            "sparc": self.sparc,
            "measured": self.measured
        }


        if self.smiles and isinstance(self.smiles, str):
            self.parent_image = Calculator().nodeWrapper(self.smiles, None, 250, 50, 'pchem_parent_wrap', 'svg', None)


        # dict with keys of checked calculators and values of
        # checked properties that are also available for said calculators
        # format: { key: "calculator name", value: [checked property ids] }
        self.checkedCalcsAndPropsDict = {}
        for calcKey, calcValue in self.calcluatorsDict.items():
            if calcValue == 'true' or calcValue == 'on':
                # get checked parameters that are available for calculator
                propList = []
                for propKey, propValue in self.checkedPropsDict.items():
                    # find checked properties
                    if propValue == 'on' or propValue == 'true':
                        # check if property is available for calculator:
                        if pchemprop_parameters.pchempropAvailable(calcKey, propKey):
                            propList.append(propKey)
                self.checkedCalcsAndPropsDict.update({calcKey: propList})
                
        self.run_data = {
            'title': "Physicochemical Properties Output",
            'jid': self.jid,
            'time': datetime.datetime.strptime(self.jid, '%Y%m%d%H%M%S%f').strftime('%A, %Y-%B-%d %H:%M:%S'),
            'chem_struct': self.chem_struct,
            'smiles': self.smiles,
            'name': self.name,
            'formula': self.formula,
            'mass': self.mass,
            'exactMass': self.exactMass
        }
