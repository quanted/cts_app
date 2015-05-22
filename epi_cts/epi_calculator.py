###########################################################
# Herein lies the map to the various calculators' queries #
###########################################################

import requests
import json
import logging
import os
from REST.calculator import Calculator
# import jchem_rest

headers = {'Content-Type': 'application/json'}


# class Calculator(object):
#     """
# 	Skeleton class for calculators
# 	NOTE: molID is recycled, always uses "7"
# 	"""
#
#     def __init__(self):
#         self.name = ''
#         self.propMap = {}  # expecting list
#         # self.baseUrl = 'http://134.67.114.6'
#         self.baseUrl = None
#         self.urlStruct = ''
#         self.results = ''
#
#     # self.postData =
#
#     @classmethod
#     def getCalcObject(self, calc):
#         return EpiCalc()
#
#
#     def getUrl(self, prop):
#         if prop in self.propMap:
#             calcProp = self.propMap[prop]['urlKey']
#             return self.urlStruct.format(calcProp)
#         else:
#             return "Error: url key not found"
#
#     def getPropKey(self, prop):
#         if prop in self.propMap:
#             return self.propMap[prop]['propKey']
#         else:
#             return "Error: prop not found"
#
#     def getResultKey(self, prop):
#         if prop in self.propMap:
#             return self.propMap[prop]['resultKey']
#         else:
#             return "Error: result key not found"
#
    # def getPostData(self, calc, prop, method=None):
    #     postData = {"smiles": ""}
    #     if calc == 'epi':
    #         return postData
    #     else:
    #         return "error!"

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



class EpiCalc(Calculator):
    """
	EPI Suite Calculator
	"""

    def __init__(self):
        Calculator.__init__(self)

        self.postData = {"smiles" : ""}
        self.name = "epi"
        self.baseUrl = os.environ['CTS_EPI_SERVER']
        # self.urlStruct = "/test/epi/calc/{}/{}" # molID, propKey
        # self.urlStruct = "/api/calculations/EpiSuite/{}"
        self.urlStruct = "/api/epiSuiteCalcs/{}"
        self.methods = None
        self.propMap = {
            'melting_point': {
                'urlKey': 'meltingPtDegCEstimated',
                'propKey': 'Melting Pt (deg C)(estimated)',
                'resultKey': 'meltingPtDegCEstimated'
            },
            'boiling_point': {
                'urlKey': 'boilingPtDegCEstimated',
                'propKey': '',
                'resultKey': 'boilingPtDegCEstimated'
            },
            'water_sol': {
                'urlKey': 'waterSolMgLEstimated',
                'propKey': '',
                'resultKey': 'waterSolMgLEstimated'
            },
            'vapor_press': {
                'urlKey': 'vaporPressMmHgEstimated',
                'propKey': '',
                'resultKey': 'vaporPressMmHgEstimated'
            },
            'henrys_law_con': {
                'urlKey': 'henryLcBondAtmM3Mole',
                'propKey': '',
                'resultKey': 'henryLcBondAtmM3Mole'
            },
            'kow_no_ph': {
                'urlKey': 'logKowEstimate',
                'propKey': '',
                'resultKey': 'logKowEstimate'
            },
        }

    def getPostData(self, calc, prop, method=None):
        return {"smiles": ""}

    def makeDataRequest(self, structure, calc, prop, method=None):
        post = self.getPostData(calc, prop)
        # post['molecule']['canonicalSmiles'] = structure
        post['smiles'] = structure
        url = self.baseUrl + self.getUrl(prop)

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

