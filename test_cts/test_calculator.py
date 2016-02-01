import requests
import json
import logging
import os
from REST.calculator import Calculator
# import jchem_rest

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
        self.urlStruct = "/api/calculations/TEST/{}/{}" # method, property

        # self.methods = ['hierarchical']
        self.methods = ['fda']
        # map workflow parameters to test
        self.propMap = {
            'melting_point': {
               'urlKey': 'MP'
            },
            'boiling_point': {
               'urlKey': 'BP'
            },
            'water_sol': {
               'urlKey': 'WS'
            },
            'vapor_press': {
               'urlKey': 'VP'
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
        url = self.baseUrl + self.urlStruct.format('hierarchical', test_prop)
        try:
            response = requests.post(url, data=json.dumps(post), headers=headers, timeout=20)
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

