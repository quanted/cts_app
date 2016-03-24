import requests
import json
import logging
import os
from REST.calculator import Calculator
from REST.smilesfilter import max_weight
from REST import smilesfilter
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
        self.urlStruct = "/rest/episuite/{}/estimated"
        self.methods = None
        self.propMap = {
            'melting_point': {
                # 'urlKey': 'meltingPtDegCEstimated',
                'urlKey': 'meltingPoint',
                'propKey': 'Melting Pt (deg C)(estimated)',
                'resultKey': 'meltingPtDegCEstimated'
            },
            'boiling_point': {
                # 'urlKey': 'boilingPtDegCEstimated',,
                'urlKey': 'boilingPoint',
                'propKey': '',
                'resultKey': 'boilingPtDegCEstimated'
            },
            'water_sol': {
                # 'urlKey': 'waterSolMgLEstimated',,
                'urlKey': 'waterSolubility',
                'propKey': '',
                'resultKey': 'waterSolMgLEstimated'
            },
            'vapor_press': {
                # 'urlKey': 'vaporPressMmHgEstimated',,
                'urlKey': 'vaporPressure',
                'propKey': '',
                'resultKey': 'vaporPressMmHgEstimated'
            },
            'henrys_law_con': {
                # 'urlKey': 'henryLcBondAtmM3Mole',,
                'urlKey': 'henrysLawConstant',
                'propKey': '',
                'resultKey': 'henryLcBondAtmM3Mole'
            },
            'kow_no_ph': {
                # 'urlKey': 'logKowEstimate',,
                'urlKey': 'logKow',
                'propKey': '',
                'resultKey': 'logKowEstimate'
            },
            'koc': {
                # 'urlKey': 'soilAdsorptionCoefKoc',,
                'urlKey': 'soilAdsorptionCoefficientKoc',
                'propKey': '',
                'resultKey': 'soilAdsorptionCoefKoc'
            }
        }

    def getPostData(self, calc, prop, method=None):
        # return {"smiles": ""} # the old way..
        # return {"identifiers":{"SMILES": ""}} # the new way..
        return {'structure': ""}

    def makeDataRequest(self, structure, calc, prop, method=None):
        post = self.getPostData(calc, prop)
        # post['smiles'] = structure # the old way..
        # post['identifiers']['SMILES'] = structure # set smiles, the new way..
        post['structure'] = structure

        url = self.baseUrl + self.getUrl(prop)

        logging.info("EPI URL: {}".format(url))

        try:
            response = requests.post(url, data=json.dumps(post), headers=headers, timeout=30)
        except requests.exceptions.ConnectionError as ce:
            logging.info("connection exception: {}".format(ce))
            raise 
        except requests.exceptions.Timeout as te:
            logging.info("timeout exception: {}".format(te))
            raise 
        else:
            self.results = response
            return response