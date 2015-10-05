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
        # return {"smiles": ""}
        return {"identifiers":{"SMILES": ""}}

    def makeDataRequest(self, structure, calc, prop, method=None):
        post = self.getPostData(calc, prop)
        post['identifiers']['SMILES'] = structure # set smiles
        # post['smiles'] = structure
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
            self.results = response
            return response

