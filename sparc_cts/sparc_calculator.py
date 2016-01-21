__author__ = 'KWOLFE'

import sys
import json
import logging
import requests
import os
from enum import Enum
import math

from REST.calculator import Calculator
from REST.calculator import CTSChemicalProperties


########################## SPARC physical properties calculator interface ###################

class SparcCalc(Calculator):
    def __init__(self, smiles=None, pressure=760.0, meltingpoint=0.0, temperature=25.0):

        self.baseUrl = os.environ['CTS_SPARC_SERVER']
        self.name = "sparc"
        self.smiles = smiles
        self.solvents = dict()
        self.pressure = pressure
        self.meltingpoint = meltingpoint
        self.temperature = temperature
        self.propMap = {
            "water_sol" : "SOLUBILITY",
            "vapor_press" : "VAPOR_PRESSURE",
            "henrys_law_con" : "HENRYS_CONSTANT",
            "mol_diss" : "DIFFUSION",
            "boiling_point": "BOILING_POINT"
        }
        self.sparc_props = [
            { 'name': "VAPOR_PRESSURE", 'units': "logAtm" },
            { 'name': "BOILING_POINT", 'units': "degreesC" },
            { 'name': "DIFFUSION", 'units': "NO_UNITS" },
            { 'name': "VOLUME", 'units': "cmCubedPerMole" },
            { 'name': "DENSITY", 'units': "gPercmCubed" },
            { 'name': "POLARIZABLITY", 'units': "angCubedPerMolecule" },
            { 'name': "INDEX_OF_REFRACTION", 'units': "dummy" },
            { 'name': "HENRYS_CONSTANT", 'units': "logAtmPerMolePerLiter" },
            { 'name': "SOLUBILITY", 'units': "mgPerLiter" },
            { 'name': "ACTIVITY", 'units': "dummy" },
            { 'name': "ELECTRON_AFFINITY", 'units': "dummy" },
            { 'name': "DISTRIBUTION", 'units': "NO_UNITS" }
        ]

    def get_sparc_query(self):
        query = {
            'pressure': self.pressure,
            'meltingpoint': self.meltingpoint,
            'temperature': self.temperature,
            'calculations': self.getCalculations(),
            'smiles': self.smiles,
            'userId': None,
            'apiKey': None,
            'type': 'MULTIPLE_PROPERTY',
            'doSolventInit': False
        }
        return query

    def get_calculation(self, sparc_prop=None, units=None):
        calc = {
            'solvents': [],
            'units': units,
            'pressure': self.pressure,
            'meltingpoint': self.meltingpoint,
            'temperature': self.temperature,
            'type': sparc_prop
        }
        return calc

    def get_solvent(self, smiles=None, name=None):
        solvent = {
            'solvents': None,
            'smiles': smiles,
            'mixedSolvent': None,
            'name': name
        }
        return solvent


    def getCalculations(self):

        calculations = list()
        calculations.append(self.get_calculation("VAPOR_PRESSURE", "logAtm")) ##############
        calculations.append(self.get_calculation("BOILING_POINT", "degreesC"))
        calculations.append(self.get_calculation("DIFFUSION", "NO_UNITS"))
        calculations.append(self.get_calculation("VOLUME", "cmCubedPerMole"))
        calculations.append(self.get_calculation("DENSITY", "gPercmCubed"))
        calculations.append(self.get_calculation("POLARIZABLITY", "angCubedPerMolecule"))
        calculations.append(self.get_calculation("INDEX_OF_REFRACTION", "dummy"))

        calcHC = self.get_calculation("HENRYS_CONSTANT", "logAtmPerMolePerLiter") ###############
        calcHC["solvents"].append(self.get_solvent("OCCCCCCCC", "octanol"))
        calculations.append(calcHC)

        calcSol = self.get_calculation("SOLUBILITY", "mgPerLiter")
        calcSol["solvents"].append(self.get_solvent("O", "water"))
        calculations.append(calcSol)

        calcAct = self.get_calculation("ACTIVITY", "dummy")
        calcAct["solvents"].append(self.get_solvent("OCCCCCCCC", "octanol"))
        calculations.append(calcAct)
        
        calculations.append(self.get_calculation("ELECTRON_AFFINITY", "dummy"))

        calcDist = self.get_calculation("DISTRIBUTION", "NO_UNITS")
        calcDist["solvents"].append(self.get_solvent("O", "water"))
        calcDist["solvents"].append(self.get_solvent("OCCCCCCCC", "octanol"))

        calculations.append(calcDist)

        return calculations


    def makeDataRequest(self):

        # Testing on local machine using static sparc response file:
        # post = self.get_sparc_query()
        # headers = {'Content-Type': 'application/json'}
        # url = self.baseUrl
        # logging.info("SPARC URL: {}".format(url))
        # logging.info("SPARC POST: {}".format(post))
        # fileout = open('C:\\Users\\nickpope\\Desktop\\sparc_response.txt', 'r')
        # response_json_string = fileout.read()
        # fileout.close()
        # logging.info("SPARC Response: {}".format(response_json_string))
        # logging.info("Type: {}".format(type(response_json_string)))
        # self.results = json.loads(response_json_string)
        # self.performUnitConversions(self.results)
        # return self.results

        # Actual calls to SPARC calculator:
        post = self.get_sparc_query()
        headers = {'Content-Type': 'application/json'}
        url = self.baseUrl

        logging.info("SPARC URL: {}".format(url))
        logging.info("sparc POST: {}".format(post))

        try:
            response = requests.post(url, data=json.dumps(post), headers=headers, timeout=30)
        except requests.exceptions.ConnectionError as ce:
            logging.info("connection exception: {}".format(ce))
            return None
        except requests.exceptions.Timeout as te:
            logging.info("timeout exception: {}".format(te))
            return None
        else:
            self.results = json.loads(response.content)
            self.performUnitConversions(self.results)
            return self.results


    def performUnitConversions(self, results_dict):
        """
        loops through sparc results, making any 
        necessary conversions
        """
        prop_data = results_dict['calculationResults']
        for prop in prop_data:
            if prop['type'] == 'VAPOR_PRESSURE':
                prop['result'] = 760.0 * math.exp(prop['result']) # log(Atm) --> mmHg
            elif prop['type'] == 'HENRYS_CONSTANT':
                prop['result'] = math.exp(prop['result']) / 1000.0 # log(atm-L/mol) --> atm-m3/mol
            # elif prop['type'] == 'SOLUBILITY':
            #     logging.info("SOLUBILITY RESULT: {}".format(prop['result']))
            #     prop['result'] = math.exp(prop['result']) # ???????? log(molefrac) --> mg/L ????????