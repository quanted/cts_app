__author__ = 'KWOLFE'

import sys
import json
from enum import Enum

class CalcTypes(Enum):
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

class Units(Enum):
    NO_UNITS = 0
    dummy = 1
    logAtm = 2
    degreesC = 3
    cmCubedPerMole = 4
    gPercmCubed = 5
    angCubedPerMolecule = 6
    logAtmPerMolePerLiter = 7
    logMolefrac = 8


class Calculation(object):
    def __init__(self, units=None, type=None, pressure=760.0, meltingpoint=0.0, temperature=25.0):
        self.solvents = dict()
        self.units = units
        self.type = type
        self.pressure = pressure
        self.meltingPoint = meltingpoint
        self.temperature = temperature


    def get_calculation(self):
        calc = dict()
        calc["solvents"] = list()
        calc["units"] = self.units
        calc["pressure"] = self.pressure
        calc["meltingPoint"] = self.meltingpoint
        calc["temperature"] = self.temperature
        calc["type"] = type

        return calc


def get_calculation(type=None, units=None, pressure=0.0, meltingpoint=0.0, temperature=0.0):
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


def get_calculations(pressure=0.0, meltingPoint=0.0, temperature=0.0):

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



class Calculations(object):
    def __init__(self):
        self.calculations = list()

        calc1 = Calculation("VAPOR_PRESSURE", "logAtm")
        self.calculations.append(calc1)

        calc2 = Calculation("BOILING_POINT", "degreesC")
        self.calculations.append(calc2)

        calc3 = Calculation("DIFFUSION", "NO_UNITS")
        self.calculations.append(calc3)

        calc4 = Calculation("VOLUME", "cmCubedPerMole")
        self.calculations.append(calc4)

        calc5 = Calculation("DENSITY", "gPercmCubed")
        self.calculations.append(calc5)

        calc6 = Calculation("POLARIZABLITY", "angCubedPerMolecule")
        self.calculations.append(calc6)

        calc7 = Calculation("INDEX_OF_REFRACTION", "dummy")
        self.calculations.append(calc7)

        calc8 = Calculation("HENRYS_CONSTANT", "logAtmPerMolePerLiter")
        solvent8 = Solvent("OCCCCCCCC", "octanol")
        calc8.solvents.append(solvent8)
        self.calculations.append(calc8)

        calc9 = Calculation("SOLUBILITY", "logMolefrac")
        solvent9 = Solvent("OCCCCCCCC", "octanol")
        calc9.solvents.append(solvent9)
        self.calculations.append(calc9)

        calc10 = Calculation("ACTIVITY", "dummy")
        solvent10 = Solvent("OCCCCCCCC", "octanol")
        calc10.solvents.append(solvent10)
        self.calculations.append(calc10)

        calc11 = Calculation("ELECTRON_AFFINITY", "dummy")
        self.calculations.append(calc11)

        calc12 = Calculation("DISTRIBUTION", "NO_UNITS")
        solvent12 = Solvent("O", "water")
        calc12.solvents.append(solvent12)
        solvent12b = Solvent("OCCCCCCCC", "octanol")
        calc12.solvents.append(solvent12b)
        self.calculations.append(calc12)

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
        if (valid = "true")
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








