###########################################################
# Herein lies the map to the various calculators' queries #
###########################################################

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
            'koc': {
                'urlKey': 'soilAdsorptionCoefKoc',
                'propKey': '',
                'resultKey': 'soilAdsorptionCoefKoc'
            }
        }

    def getPostData(self, calc, prop, method=None):
        # return {"smiles": ""}
        return {"identifiers":{"SMILES": ""}}

    def makeDataRequest(self, structure, calc, prop, method=None):
        post = self.getPostData(calc, prop)

        # run structure through epi suite smiles filter..
        logging.info("filtering smiles for epi suite...")
        # structure = smilesFilter(structure) # make sure mass is < 1500g/mol
        structure = smilesfilter.parseSmilesByCalcultor(structure, calc)

        post['identifiers']['SMILES'] = structure # set smiles
        # post['smiles'] = structure

        url = self.baseUrl + self.getUrl(prop)

        try:
            response = requests.post(url, data=json.dumps(post), headers=headers, timeout=120)
        except requests.exceptions.ConnectionError as ce:
            logging.info("connection exception: {}".format(ce))
            raise 
        except requests.exceptions.Timeout as te:
            logging.info("timeout exception: {}".format(te))
            raise 
        else:
            self.results = response
            return response

# def smilesFilter(structure):
#         """
#         EPI Suite dependent SMILES filtering!
#         """
#         from chemaxon_cts import jchem_rest

#         request = requests.Request()
#         request.data = { 'smiles': structure }

#         response = jchem_rest.getMass(request) # get mass from jchem ws
#         json_obj = json.loads(response.content)

#         # 1. check mass..
#         struct_mass = json_obj['data'][0]['mass']
#         if struct_mass > max_weight or struct_mass < 0:
#             raise Exception("chemical mass exceeds limit..")

#         # 2. now clear stereos from structure..
#         response = jchem_rest.clearStereo(request)
#         request.data = { 'chemical': response.content } # structure in mrv format

#         response = jchem_rest.convertToSMILES(request) # mrv >> smiles
#         filtered_smiles = json.loads(response.content)['structure'] # get stereoless structure

#         # 3. transform [N+](=O)[O-] >> N(=O)=O..
#         request.data = { 'smiles': filtered_smiles }
#         response = jchem_rest.transform(request)

#         request.data = { 'chemical': filtered_smiles }
#         response = jchem_rest.convertToSMILES(request)
#         filtered_smiles = json.loads(response.content)['structure']

#         logging.info(">>> EPI SUITE FILTERED SMILES: {}".format(filtered_smiles))

#         return filtered_smiles