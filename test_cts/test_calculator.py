import requests
import json
import logging
import os
from REST.calculator import Calculator

headers = {'Content-Type': 'application/json'}


class TestCalc(Calculator):
    """
	TEST Suite Calculator
	"""

    def __init__(self):
        Calculator.__init__(self)

        self.postData = {"smiles" : ""}
        self.name = "test"
        self.baseUrl = os.environ['CTS_TEST_SERVER']
        # self.urlStruct = "/api/epiSuiteCalcs/{}"
        self.urlStruct = "/api/TEST/{}/{}" # method, property

        # self.methods = ['hierarchical']
        self.methods = ['FDAMethod', 'HierarchicalMethod']
        # map workflow parameters to test
        self.propMap = {
            'melting_point': {
               'urlKey': 'MeltingPoint'
            },
            'boiling_point': {
               'urlKey': 'BoilingPoint'
            },
            'water_sol': {
               'urlKey': 'WaterSolubility'
            },
            'vapor_press': {
               'urlKey': 'VaporPressure'
            }
            # 'henrys_law_con': ,
            # 'kow_no_ph': 
        }

    def getPostData(self, calc, prop, method=None):
        return {"identifiers": {"SMILES": ""}}

    def makeDataRequest(self, structure, calc, prop, method=None):
        post = self.getPostData(calc, prop)
        post['identifiers']['SMILES'] = structure # set smiles
        test_prop = self.propMap[prop]['urlKey'] # prop name TEST understands
        url = self.baseUrl + self.urlStruct.format('FDAMethod', test_prop)
        try:
            response = requests.post(url, data=json.dumps(post), headers=headers, timeout=60)
        except requests.exceptions.ConnectionError as ce:
            logging.info("connection exception: {}".format(ce))
            # return None
            raise
        except requests.exceptions.Timeout as te:
            logging.info("timeout exception: {}".format(te))
            # return None
            raise

        self.results = response
        return response

