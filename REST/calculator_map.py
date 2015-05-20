###########################################################
# Herein lies the map to the various calculators' queries #
###########################################################

import requests
import json
import logging
import os
# import jchem_rest

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
        self.baseUrl = os.environ['CTS_TEST_SERVER']
        self.urlStruct = ''
        self.results = ''

    # self.postData =

    @classmethod
    def getCalcObject(self, calc):
        if calc == 'chemaxon':
            return ChemaxonCalc()
        elif calc == 'test':
            return TestCalc()
        elif calc == 'epi':
            return EpiCalc()
        elif calc == 'measured':
            return MeasuredCalc()
        elif calc == 'sparc':
            return MeasuredCalc()
        else:
            raise TypeError('Valid calculators are chemaxon, test, epi, and measured')

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

    def getPostData(self, calc, prop, method=None):
        postData = {
            # "molecule": {
            #     "inChIKey": "",
            #     "iupacName": "",
            #     "inChI": "",
            #     "canonicalSmiles": ""
            # }
            "smiles": ""
        }
        if calc == 'epi':
            return postData
        elif calc == 'test':
            # logging.info(propMap)
            postData.update({
                "property": self.propMap[prop]['propKey'],
                "method": "hierarchical"
            })
            return postData
        else:
            return "error!"

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


# class TestCalc(Calculator):
#     """
# 	TEST Calculator
# 	"""
#
#     def __init__(self):
#
#         Calculator.__init__(self)
#
#         # self.urlStruct = "/test/test/calc/{}/{}/{}" # molID, propKey, method
#         self.urlStruct = "/api/calculations/TEST/HierarchicalMethod/{}"
#         self.methods = ['hierarchical']  # accounting for one method atm
#         self.name = "test"
#         self.propMap = {
#             'melting_point': {
#                 'urlKey': 'MeltingPoint',
#                 'propKey': 'mp',
#                 'resultKey': 'meltingPointTESTHierarchical',
#             },
#             'boiling_point': {
#                 'urlKey': 'BoilingPoint',
#                 'propKey': 'bp',
#                 'resultKey': 'boilingPointTESTHierarchical'
#             },
#             'water_sol': {
#                 'urlKey': 'WaterSolubility',
#                 'propKey': 'ws',
#                 'resultKey': 'waterSolubilityTESTHierarchical'
#             },
#             'vapor_press': {
#                 'urlKey': 'VaporPressure',
#                 'propKey': 'vp',
#                 'resultKey': 'vaporPressureTESTHierarchical'
#             }
#         }
#
#     def getPchemPropData(self, propKey):
#         try:
#             if propKey in self.propMap:
#                 req = requests.Request(data={'calc': 'test', 'prop': propKey})
#                 return epi_cts.views.less_simple_proxy(req)
#             else:
#                 raise  # ?
#         except KeyError:
#             print "Property does not exist in TEST"


class EpiCalc(Calculator):
    """
	EPI Suite Calculator
	"""

    def __init__(self):
        Calculator.__init__(self)

        self.name = "epi"
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


class MeasuredCalc(Calculator):
    """
	Measured Data (technically not a calculator)
	"""

    def __init__(self):
        Calculator.__init__(self)

        # self.urlStruct = "/test/measured/{}/test/{}"  # molID, propKey
        self.urlStruct = "/api/calculations/measured/{}"
        self.methods = None
        self.propMap = {
            'melting_point': {
                'urlKey': 'meltingPoint',
                'resultKey': 'measuredMeltingPoint',
            },
            'boiling_point': {
                'urlKey': 'boilingPoint',
                'resultKey': 'measuredBoilingPoint'
            },
            'water_sol': {
                'urlKey': 'waterSolubility',
                'resultKey': 'measuredWaterSolubility'
            },
            'vapor_press': {
                'urlKey': 'vaporPressure',
                'resultKey': 'measuredVaporPressure'
            }
        }


class ChemaxonCalc(Calculator):
    """
	ChemAxon Calculator
	NOTE: see jchem_rest instead
	"""

    def __init__(self):
        Calculator.__init__(self)
        self.metabolizerUrl = "/efsws/rest/metabolizer"  # TODO: figure out better book keeping for urls
        self.urlStruct = "/webservices/rest-v0/util/calculate/{}"
        self.name = "chemaxon"

        # NOTE: would it make sense to map urlKeys to jchem_rest functions?
        # Or do another way I haven't thought of yet?
        self.propMap = {
            'water_sol': {
                'urlKey': 'solubility',
                'resultKey': ''
            },
            'ion_con': {
                'urlKey': 'pKa',
                'resultKey': ''
            },
            'kow_no_ph': {
                'urlKey': 'logD',
                'resultKey': '',
                'methods': ['KLOP', 'VG', 'PHYS']
            },
            'kow_wph': {
                'urlKey': 'logP',
                'resultKey': '',
                'methods': ['KLOP', 'VG', 'PHYS']
            }
        }

class SPARCCalc(Calculator):
    """
	SPARC Calculator
	"""

    def __init__(self):
        Calculator.__init__(self)

        self.name = "sparc"
        # self.urlStruct = "/test/epi/calc/{}/{}" # molID, propKey
        self.urlStruct = "http://archemcalc.com/sparc-integration/rest/calc/multiProperty"
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