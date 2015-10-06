__author__ = 'KWOLFE'

import sys
import json
import logging
import requests
import os
from enum import Enum

from REST.calculator import Calculator
from REST.calculator import CTSChemicalProperties


class SPARCChemicalProperties(Enum):
    NONE = 0
    VAPOR_PRESSURE = 1
    BOILING_POINT = 2
    DIFFUSION = 3
    VOLUME = 4
    DENSITY = 5
    POLARIZABLITY = 6
    INDEX_OF_REFRACTION = 7
    HENRYS_CONSTANT = 8
    SOLUBILITY = 9
    ACTIVITY = 10
    ELECTRON_AFFINITY = 11
    DISTRIBUTION = 12
    MULTIPLE_PROPERTY = 13

class SPARCChemicalPropertyUnits(Enum):
    NO_UNITS = 0
    dummy = 1
    logAtm = 2
    degreesC = 3
    cmCubedPerMole = 4
    gPercmCubed = 5
    angCubedPerMolecule = 6
    logAtmPerMolePerLiter = 7
    logMolefrac = 8

chemPropMap = {
    "water_sol" : "SOLUBILITY",
    "vapor_press" : "VAPOR_PRESSURE",
    "henrys_law_con" : "HENRYS_CONSTANT",
    "mol_diss" : "DIFFUSION",
    "boiling_point": "BOILING_POINT"
}

########################## SPARC physical properties calculator interface ###################

class SPARC_Calc(Calculator):
    def __init__(self, smiles, pressure=760.0, meltingpoint=0.0, temperature=25.0):

        self.baseUrl = os.environ['CTS_SPARC_SERVER']

        self.name = "sparc"
        self.smiles = smiles
        self.solvents = dict()
        self.pressure = pressure
        self.meltingPoint = meltingpoint
        self.temperature = temperature

    def get_sparc_query(self):
        query = dict()
        query["pressure"] = self.pressure
        query["meltingPoint"] = self.meltingPoint
        query["temperature"] = self.temperature
        query["calculations"] = get_calculations()

        query["smiles"] = self.smiles
        query["userId"] = None
        query["apiKey"] = None
        query["type"] = "MULTIPLE_PROPERTY"
        query["doSolventInit"] = False

        return query


    def get_calculations(self):

        calculations = list()
        # calculations.append(get_calculation("VAPOR_PRESSURE", "logAtm")) ##############
        calculations.append(get_calculation("VAPOR_PRESSURE", "log(atm)")) # attempt to fix unit mismatch
        calculations.append(get_calculation("BOILING_POINT", "degreesC"))

        calculations.append(get_calculation("DIFFUSION", "NO_UNITS"))

        calculations.append(get_calculation("VOLUME", "cmCubedPerMole"))

        calculations.append(get_calculation("DENSITY", "gPercmCubed"))

        calculations.append(get_calculation("POLARIZABLITY", "angCubedPerMolecule"))

        calculations.append(get_calculation("INDEX_OF_REFRACTION", "dummy"))

        # calcHC = get_calculation("HENRYS_CONSTANT", "logAtmPerMolePerLiter") ###############
        calcHC = get_calculation("HENRYS_CONSTANT", "atm/(mol/m^3)") # attempt to fix unit mismatch
        calcHC["solvents"].append(get_solvent("OCCCCCCCC", "octanol"))
        calculations.append(calcHC)

        # calcSol = get_calculation("SOLUBILITY", "logMolefrac") ###########
        calcSol = get_calculation("SOLUBILITY", "mg/l") # attempt to fix unit mismatch
        calcSol["solvents"].append(get_solvent("OCCCCCCCC", "octanol"))
        calculations.append(calcSol)

        calcAct = get_calculation("ACTIVITY", "dummy")
        calcAct["solvents"].append(get_solvent("OCCCCCCCC", "octanol"))
        calculations.append(calcAct)

        calculations.append(get_calculation("ELECTRON_AFFINITY", "dummy"))

        calcDist = get_calculation("DISTRIBUTION", "NO_UNITS")
        calcDist["solvents"].append(get_solvent("O", "water"))
        calcDist["solvents"].append(get_solvent("OCCCCCCCC", "octanol"))
        calculations.append(calcDist)

        return calculations



    def get_calculation(self, type=None, units=None):
        calc = dict()
        calc["solvents"] = list()
        calc["units"] = units
        calc["pressure"] = self.pressure
        calc["meltingPoint"] = self.meltingpoint
        calc["temperature"] = self.temperature
        calc["type"] = type

        return calc


    def makeDataRequest(self):

        post = self.get_sparc_query()

        headers = {'Content-Type': 'application/json'}
        # post['molecule']['canonicalSmiles'] = structure
        #post['smiles'] = structure
        url = self.baseUrl

        logging.info("url: {}".format(url))

        try:
            response = requests.post(url, data=json.dumps(post), headers=headers, timeout=120)
        except requests.exceptions.ConnectionError as ce:
            logging.info("connection exception: {}".format(ce))
            return None
        except requests.exceptions.Timeout as te:
            logging.info("timeout exception: {}".format(te))
            return None
        else:
            self.results = json.loads(response.content)
            return self.results


    def getPropertyValue(self, prop):
        result = ""

        if self.results == None:
            return None

        if prop in chemPropMap.keys():
            sparcProp = chemPropMap[prop] # get key sparc understands
        else:
            return None

        calcResults = self.results["calculationResults"] # list of prop results
        for prop in calcResults:
            if prop["type"] == sparcProp:
                return prop["result"] # return prop value

        return None




#  -----------------------End Class SPARC_Calculator----------------------------

def get_calculation(type=None, units=None, pressure=760.0, meltingpoint=0.0, temperature=25.0):
    calc = dict()
    calc["solvents"] = list()
    calc["units"] = units
    calc["pressure"] = pressure
    calc["meltingPoint"] = meltingpoint
    calc["temperature"] = temperature
    calc["type"] = type

    return calc

def get_solvent(smiles=None, name=None):
    solvent = dict()
    solvent["solvents"] = None
    solvent["smiles"] = smiles
    solvent["mixedSolvent"] = None
    solvent["name"] = name

    return solvent


def get_calculations(pressure=760.0, meltingPoint=0.0, temperature=25.0):

    p = pressure
    m = meltingPoint
    t = temperature

    calculations = list()
    calculations.append(get_calculation("VAPOR_PRESSURE", "logAtm", p, m, t))
    calculations.append(get_calculation("BOILING_POINT", "degreesC", p, m, t))

    calculations.append(get_calculation("DIFFUSION", "NO_UNITS", p, m, t))

    calculations.append(get_calculation("VOLUME", "cmCubedPerMole", p, m, t))

    calculations.append(get_calculation("DENSITY", "gPercmCubed", p, m, t))

    calculations.append(get_calculation("POLARIZABLITY", "angCubedPerMolecule", p, m, t))

    calculations.append(get_calculation("INDEX_OF_REFRACTION", "dummy", p, m, t))

    calcHC = get_calculation("HENRYS_CONSTANT", "logAtmPerMolePerLiter", p, m, t)
    calcHC["solvents"].append(get_solvent("OCCCCCCCC", "octanol"))
    calculations.append(calcHC)

    calcSol = get_calculation("SOLUBILITY", "logMolefrac", p, m, t)
    calcSol["solvents"].append(get_solvent("OCCCCCCCC", "octanol"))
    calculations.append(calcSol)

    calcAct = get_calculation("ACTIVITY", "dummy", p, m, t)
    calcAct["solvents"].append(get_solvent("OCCCCCCCC", "octanol"))
    calculations.append(calcAct)

    calculations.append(get_calculation("ELECTRON_AFFINITY", "dummy", p, m, t))

    calcDist = get_calculation("DISTRIBUTION", "NO_UNITS", p, m, t)
    calcDist["solvents"].append(get_solvent("O", "water"))
    calcDist["solvents"].append(get_solvent("OCCCCCCCC", "octanol"))
    calculations.append(calcDist)

    return calculations


def get_sparc_query(smiles, pressure=760.0, meltingPoint=0.0, temperature=25.0):
    query = dict()
    query["pressure"] = pressure
    query["meltingPoint"] = meltingPoint
    query["temperature"] = temperature
    query["calculations"] = get_calculations(pressure, meltingPoint, temperature)

    query["smiles"] = smiles
    query["userId"] = None
    query["apiKey"] = None
    query["type"] = "MULTIPLE_PROPERTY"
    query["doSolventInit"] = False

    return query


def parse_sparc_result(sparc_result):
    try:
        dict_result = json.loads(sparc_result)
    except ValueError, e:
        print "Parse error"
        return False

    def get_calculation(self):
        return self.calculations



class Solvent(object):
    def __init__(self, smiles=None, name=None):
        self.smiles = smiles
        self.name = name
        self.mixedSolvent = False
        self.solvent = None

    def get_solvent(self):
        solvent = dict()
        solvent["solvents"] = None
        solvent["smiles"] = self.smiles
        solvent["mixedSolvent"] = None
        solvent["name"] = self.name

        return solvent



class SparcQuery(object):
    def __init__(self, smiles, pressure, melting_point, temperature):
        self.smiles = smiles
        self.pressure = pressure
        self.meltingPoint = melting_point
        self.temperature = temperature
        self.type = "MULTIPLE_PROPERTY"
        self.userId = None
        self.apiKey = None
        self.doSolventInit = False
        self.calculations = []
        self.solvents = []

        calcs = Calculations()
        self.calculations = calcs.calculations

        for calc in self.calculations:
            calc.pressure = self.pressure
            calc.meltingPoint = self.meltingPoint
            calc.temperature = self.temperature



class SPARCResult(object):
    def __init__(self):
        self.valid = False
        self.smiles = ""
        self.pressure = 0.0
        self.meltingPoint = 0.0
        self.temperature = 0.0
        self.molWeight = 0.0
        self.type = "MULTIPLE_PROPERTY"
        self.userId = None
        self.apiKey = None
        self.doSolventInit = False
        self.calculationResults = []
        self.solvents = []
        self.results = dict()

    def parseSPARCResult(self, sparc_result):
        try:
            self.results = json.loads(sparc_result)
        except ValueError:
            return False

        valid = self.results["valid"]
        if valid == "true":
            self.valid = True
        self.type = self.results["type"]
        self.smiles = self.results["smiles"]
        self.userId = self.results["userId"]
        self.apiKey = self.results["apiKey"]
        self.meltingPoint = self.results["meltingPoint"]
        self.temperature = self.results["temperature"]
        self.pressure = self.results["pressure"]
        self.molWeight = self.results["molWeight"]
        self.calculationResults = self.results["calculationResults"]