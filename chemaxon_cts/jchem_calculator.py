__author__ = 'np'

"""
Classes for jchem ws p-chem and other properties.
Intended to match the structure of the other
calculator classes.
"""

import requests
import json
import logging
import os
from jchem_rest import getStructInfo

headers = {'Content-Type': 'application/json'}


class JchemProperty(object):
    def __init__(self):
        self.propsList = ['pKa', 'isoelectricPoint', 'majorMicrospecies', 'tautomerization', 'stereoisomer']
        self.baseUrl = os.environ['CTS_JCHEM_SERVER']
        self.name = ''
        self.url = ''
        self.structure = ''  # cas, smiles, iupac, etc.
        self.postData = {}
        self.results = ''
        self.propMap = {
            'water_sol': [],
            'ion_con': [], 
            'kow_no_ph': [],
            'kow_wph': []
        }

    def setPostDataValue(self, propKey, propValue):
        """
		Can set one key:value with (propKey, propValue)
		"""
        try:
            self.postData[propKey] = propValue
        except KeyError as ke:
            logging.warning("key {} does not exist".format(propKey))
            raise
        except Exception as e:
            logging.warning("error occured: {}".format(e))
            return None

    def setPostDataValues(self, multiKeyValueDict):
        """
		Can set multiple key:values at once w/ dict
		"""
        try:
            for key, value in multiKeyValueDict.items():
                self.postData[key] = value
        except KeyError as ke:
            logging.warning("key {} does not exist".format(key))
            return None
        except Exception as e:
            logging.warning("error occured: {}".format(e))
            return None

    def makeDataRequest(self, structure):
        url = self.baseUrl + self.url
        self.postData.update({
            "result-display": {
                "include": ["structureData", "image"],
                "parameters": {
                    "structureData": "smiles"
                }
            }
        })
        postData = {
            "structure": structure,
            "parameters": self.postData
        }
        try:
            response = requests.post(url, data=json.dumps(postData), headers=headers, timeout=60)
            self.results = json.loads(response.content)
            return response
        except ValueError as ve:
            logging.warning("> error decoding json: {}".format(ve))
            raise ValueError("error decoding json")
        except requests.exceptions.RequestException as err:
            raise err

    @classmethod
    def getPropObject(self, prop):
        """
		For getting prop objects in a general,
		loop-friendly way
		"""
        if prop == 'pKa':
            return Pka()
        elif prop == 'isoelectricPoint':
            return IsoelectricPoint()
        elif prop == 'majorMicrospecies':
            return MajorMicrospecies()
        elif prop == 'tautomerization':
            return Tautomerization()
        elif prop == 'stereoisomer':
            return Stereoisomer()
        elif prop == 'solubility':
            return Solubility()
        elif prop == 'logP':
            return LogP()
        elif prop == 'logD':
            return LogD()
        else:
            raise ValueError("property object request does not exist")


class Pka(JchemProperty):
    def __init__(self):
        JchemProperty.__init__(self)
        self.name = 'pKa'
        self.url = '/webservices/rest-v0/util/calculate/pKa'
        self.postData = {
            "pHLower": 0.0,
            "pHUpper": 14.0,
            "pHStep": 0.1,
            "temperature": 298.0,
            "micro": False,
            "considerTautomerization": True,
            "pKaLowerLimit": -20.0,
            "pKaUpperLimit": 10.0,
            "prefix": "DYNAMIC"
        }

    def getMostAcidicPka(self):
        """
		Picks out pKa acidic value(s), returns list
		"""
        pkaValList = []
        if 'mostAcidic' in self.results:
            # logging.info("$ type: {} $".format(self.results['mostAcidic']))
            for pkaVal in self.results['mostAcidic']:
                pkaValList.append(pkaVal)
            return pkaValList
        else:
            logging.warning("key: 'mostAcidic' not in self.results")
            return None

    def getMostBasicPka(self):
        """
		Picks out pKa Basic value(s), returns list
		"""
        pkaValList = []
        if 'mostBasic' in self.results:
            for pkaVal in self.results['mostBasic']:
                pkaValList.append(pkaVal)
            return pkaValList
        else:
            logging.warning("no key 'mostBasic' in results")
            return None

    def getParent(self):
        """
		Gets parent image from result and adds structure
		info such as formula, iupac, mass, and smiles.
		Returns dict with keys: image, formula, iupac, mass, and smiles
		"""
        try:
            parentDict = {'image': self.results['result']['image']['image'], 'key': 'parent'}
            parentDict.update(getStructInfo(self.results['result']['structureData']['structure']))
            return parentDict
        except KeyError as ke:
            logging.warning("key error: {}".format(ke))
            return None

    def getMicrospecies(self):
        """
		Gets microspecies from pKa result and appends 
		structure info (i.e., formula, iupac, mass, and smiles)
		Returns list of microspeceies as dicts
		with keys: image, formula, iupac, mass, and smiles
		"""
        if 'microspecies' in self.results:
            try:
                msList = []
                for ms in self.results['microspecies']:
                    msStructDict = {}  # list element in msList
                    msStructDict.update({'image': ms['image']['image'], 'key': ms['key']})
                    structInfo = getStructInfo(ms['structureData']['structure'])
                    msStructDict.update(structInfo)
                    msList.append(msStructDict)
                return msList
            except KeyError as ke:
                logging.info("> key error: {}".format(ke))
                return None
        else:
            logging.info("no microspecies in results")
            return None

    def getChartData(self):
        if 'chartData' in self.results:
            microDistData = {}  # microspecies distribution data
            for ms in self.results['chartData']:
                valuesList = []  # format: [[ph1,con1], [ph2, con2], ...] per ms
                for vals in ms['values']:
                    xy = []  # [ph1, con1]
                    xy.append(vals['pH'])
                    xy.append(100.0 * vals['concentration'])  # convert to %
                    valuesList.append(xy)
                microDistData.update({ms['key']: valuesList})
            return microDistData
        else:
            return None


class IsoelectricPoint(JchemProperty):
    def __init__(self):
        JchemProperty.__init__(self)
        self.name = 'isoelectricPoint'
        self.url = '/webservices/rest-v0/util/calculate/isoelectricPoint'
        self.postData = {
            "pHStep": 0.1,
            "doublePrecision": 2
        }

    def getIsoelectricPoint(self):
        """
		Returns isoelectricPoint value from results
		"""
        try:
            return self.results['isoelectricPoint']
        except KeyError:
            logging.warning("key 'isoelectricPoint' not in results")
            return None

    def getIsoPtChartData(self):
        """
		Returns isoelectricPoint chart data
		"""
        valsList = []
        try:
            for pt in self.results['chartData']['values']:
                xyPair = []
                for key, value in pt.items():
                    xyPair.append(value)
                valsList.append(xyPair)
        except KeyError as ke:
            logging.warning("key error: {}".format(ke))
            return valsList
        else:
            return valsList


class MajorMicrospecies(JchemProperty):
    def __init__(self):
        JchemProperty.__init__(self)
        self.name = 'majorMicrospecies'
        self.url = '/webservices/rest-v0/util/calculate/majorMicrospecies'
        self.postData = {
            "pH": 7.4,
            "takeMajorTautomericForm": False
        }

    def getMajorMicrospecies(self):
        majorMsDict = {}
        try:
            majorMsDict.update({'image': self.results['result']['image']['image'], 'key': 'majorMS'})
            structInfo = getStructInfo(self.results['result']['structureData']['structure'])
            majorMsDict.update(structInfo)  # add smiles, iupac, mass, formula key:values
            return majorMsDict
        except KeyError as ke:
            logging.warning("key error: {}".format(ke))
            return None


class Tautomerization(JchemProperty):
    def __init__(self):
        JchemProperty.__init__(self)
        self.name = 'tautomerization'
        self.url = '/webservices/rest-v0/util/calculate/tautomerization'
        self.postData = {
            "calculationType": "DOMINANT",
            "maxStructureCount": 1000,
            "considerPH": False,
            "enableMaxPathLength": True,
            "maxPathLength": 4,
            "rationalTautomerGenerationMode": False,
            "singleFragmentMode": True,
            "protectAromaticity": True,
            "protectCharge": True,
            "excludeAntiAromaticCompounds": True,
            "protectDoubleBondStereo": False,
            "protectAllTetrahedralStereoCenters": False,
            "protectLabeledTetrahedralStereoCenters": False,
            "protectEsterGroups": True,
            "ringChainTautomerizationAllowed": False
        }

    def getTautomers(self):
        """
        returns dict w/ key 'tautStructs' and
        value is a list of tautomer images
        """
        tautDict = {'tautStructs': [None]}
        tautImageList = []
        try:
            for taut in self.results['result']:
                tautStructDict = {'image': taut['image']['image'], 'key': 'taut'}
                structInfo = getStructInfo(taut['structureData']['structure'])
                tautStructDict.update(structInfo)
                tautStructDict.update({'dist': 100 * round(taut['dominantTautomerDistribution'], 4)})
                tautImageList.append(tautStructDict)
            tautDict.update({'tautStructs': tautImageList})
            return tautImageList
        except KeyError as ke:
            logging.warning("key error: {}".format(ke))
            return None


class Stereoisomer(JchemProperty):
    def __init__(self):
        JchemProperty.__init__(self)
        self.name = 'stereoisomer'
        self.url = '/webservices/rest-v0/util/calculate/stereoisomer'
        self.postData = {
            "stereoisomerismType": "TETRAHEDRAL",
            "maxStructureCount": 100,
            "protectDoubleBondStereo": False,
            "protectTetrahedralStereo": False,
            "filterInvalid3DStructures": False
        }

    def getStereoisomers(self):
        stereoList = []
        try:
            for stereo in self.results['result']:
                stereoDict = {'image': stereo['image']['image'], 'key': 'stereo'}
                structInfo = getStructInfo(stereo['structureData']['structure'])
                stereoDict.update(structInfo)
                stereoList.append(stereoDict)
            return stereoList
        except KeyError as ke:
            logging.warning("key error: {} @ jchem rest".format(ke))
            return None


class Solubility(JchemProperty):
    def __init__(self):
        JchemProperty.__init__(self)
        self.name = 'solubility'
        self.url = '/webservices/rest-v0/util/calculate/solubility'
        self.postData = {
            "pHLower": 0.0,
            "pHUpper": 14.0,
            "pHStep": 0.1,
            "unit": "MGPERML"
        }

    def getSolubility(self):
        """
		Gets water solubility for chemaxon
		"""
        try:
            return 1000.0 * self.results['intrinsicSolubility']
        except KeyError as ke:
            logging.warning("key error: {}".format(ke))
            return None


class LogP(JchemProperty):
    def __init__(self):
        JchemProperty.__init__(self)
        self.name = 'logP'
        self.url = '/webservices/rest-v0/util/calculate/logP'
        self.postData = {
            "method": "WEIGHTED",
            "wVG": 1.0,
            "wKLOP": 1.0,
            "wPHYS": 1.0,
            "Cl": 0.1,
            "NaK": 0.1,
            "considerTautomerization": False
        }

    def getLogP(self):
        """
		Gets pH-independent kow
		"""
        try:
            return self.results['logpnonionic']
        except KeyError as ke:
            logging.warning("ker error: {}".format(ke))
            return None


class LogD(JchemProperty):
    def __init__(self):
        JchemProperty.__init__(self)
        self.name = 'logD'
        self.url = '/webservices/rest-v0/util/calculate/logD'
        self.postData = {
            "pHLower": 0.0,
            "pHUpper": 14.0,
            "pHStep": 0.1,
            "method": "WEIGHTED",
            "wVG": 1.0,
            "wKLOP": 1.0,
            "wPHYS": 1.0,
            "Cl": 0.1,
            "NaK": 0.1,
            "considerTautomerization": False
        }

    def getLogD(self, ph):
        """
		Gets pH-dependent kow
		"""
        try:
            ph = float(ph)
            chartDataList = self.results['chartData']['values']
            for xyPair in chartDataList:
                if xyPair['pH'] == round(ph, 1):
                    value = xyPair['logD']
                    break
            return value
        except KeyError as ke:
            logging.warning("key error: {}".format(ke))
            return None