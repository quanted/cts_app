__author__ = 'np'


import requests
import json
import logging
import os
from enum import Enum

class CTSChemicalProperties(Enum):
    boiling_point  = 0
    melting_point  = 1
    water_sol      = 3
    vapor_press    = 4
    mol_diss       = 5
    ion_con        = 6
    henrys_law_con = 7
    kow_no_ph      = 8
    kow_wph        = 9
    kow_ph         = 10
    kow            = 11


headers = {'Content-Type': 'application/json'}

class Calculator(object):
    """
	Skeleton class for calculators
	NOTE: molID is recycled, always uses "7"
	"""

    def __init__(self):
        self.name = ''
        self.propMap = {}  # expecting list
        # self.baseUrl = 'http://134.67.114.6'
        self.baseUrl = None
        self.urlStruct = ''
        self.results = ''

    # self.postData =

    # @classmethod
    # def getCalcObject(self, calc):
    #     return EpiCalc()


    def getUrl(self, prop):
        if prop in self.propMap:
            calcProp = self.propMap[prop]['urlKey']
            return self.urlStruct.format(calcProp)
        else:
            return "Error: url key not found"

    def getPropKey(self, prop):
        if prop in self.propMap:
            return self.propMap[prop]['propKey']
        else:
            return "Error: prop not found"

    def getResultKey(self, prop):
        if prop in self.propMap:
            return self.propMap[prop]['resultKey']
        else:
            return "Error: result key not found"

    # def getPostData(self, calc, prop, method=None):
    #     postData = {"smiles": ""}
    #     if calc == 'epi':
    #         return postData
    #     else:
    #         return "error!"
    #
    # def makeDataRequest(self, structure, calc, prop, method=None):
    #     post = self.getPostData(calc, prop)
    #     # post['molecule']['canonicalSmiles'] = structure
    #     post['smiles'] = structure
    #     url = self.baseUrl + self.getUrl(prop)
    #
    #     logging.info("url: {}".format(url))
    #
    #     try:
    #         response = requests.post(url, data=json.dumps(post), headers=headers, timeout=120)
    #     except requests.exceptions.ConnectionError as ce:
    #         logging.info("connection exception: {}".format(ce))
    #         return None
    #     except requests.exceptions.Timeout as te:
    #         logging.info("timeout exception: {}".format(te))
    #         return None
    #     else:
    #         self.results = json.loads(response.content)
    #         return self.results
