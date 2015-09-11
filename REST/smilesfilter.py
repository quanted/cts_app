__author__ = 'KWOLFE'

from chemaxon_cts import jchem_rest
import requests
import logging
import json
from chemaxon_cts.jchem_rest import JchemProperty as JProp


def is_valid_smiles(smiles):

    excludestring = {".",
                         "[Ag]",
                         "[Al]",
                         "[Au]",
                         "[As]",
                         "[As+",
                         "[B]",
                         "[B-]",
                         "[Br-]",
                         "[Ca]",
                         "[Ca+",
                         "[Cl-]",
                         "[Co]",
                         "[Co+",
                         "[Fe]",
                         "[Fe+",
                         "[Hg]",
                         "[K]",
                         "[K+",
                         "[Li]",
                         "[Li+",
                         "[Mg]",
                         "[Mg+",
                         "[Na]",
                         "[Na+",
                         "[Pb]",
                         "[Pb2+]",
                         "[Pb+",
                         "[Pt]",
                         "[Sc]",
                         "[Si]",
                         "[Si+",
                         "[SiH]",
                         "[Sn]",
                         "[W]"
                                }


    return_val = {
            "valid" : False,
            "smiles": smiles,
            "processedsmiles" : ""
    }
    if any(x in smiles for x in excludestring):
        return return_val
    else:
        processed_smiles = filterSMILES(smiles)
        return_val["valid"] = True
        return_val["processedsmiles"] = processed_smiles
        return return_val


def filterSMILES(smiles):
    """
    calls jchem web services through jchem_rest 
    """
    
    request = requests.Request(data={'smiles': smiles}) # wrap smiles in http request
    response = jchem_rest.filterSMILES(request)
    logging.info("RESPONSE: {}".format(response.content))

    try:
        filtered_smiles = json.loads(response.content)['result'][0] # picks out smiles from efs???
        logging.info("NEW SMILES: {}".format(filtered_smiles))
        return filtered_smiles
    except Exception as e:
        logging.info("> error in filterSMILES: {}".format(e))
        raise e


# def dehydrogenizeSMILES(smiles):
#     """
#     calls jchem web services through jchem_rest 
#     """
#     request = requests.Request(data={'smiles': smiles}) # wrap smiles in http request
#     response = jchem_rest.removeExplicitHFromSMILES(request)
#     logging.info("RESPONSE: {}".format(response.content))
#     try:
#         # dehydrogenized_smiles = response.json.get('structure')
#         dehydrogenizeSMILES = json.loads(response.content)['structure']
#         logging.info("NEW SMILES: {}".format(dehydrogenizeSMILES))
#         return dehydrogenizeSMILES
#     except Exception as e:
#         logging.info("> dehydrogenize in smilesfilter error: {}".format(e))
#         raise e


# def transformSMILES(smiles):
#     """
#     transforms SMILES string based on:
#     N(=O)=O --> [N+](=O)[O-]
#     """
#     request = requests.Request(data={'smiles': smiles})
#     response = jchem_rest.transformSMILES(request)



# def getDominateTautomer(smiles):
#     """
#     calls jchem_rest tautomer code, returns smiles
#     of dominant tautomer from jchem ws response
#     """

#     taut_obj = JProp.getPropObject('tautomerization')
#     # taut_obj.setPostDataValues({
#         # "maxStructureCount": self.tautomer_maxNoOfStructures,
#         # "pH": self.tautomer_pH,
#         # "considerPH": True
#     # })
#     taut_obj.makeDataRequest(smiles)
#     logging.info("taut results: {}".format(taut_obj.results))

#     try:
#         dominant_taut = taut_obj.results['result'][0]['structureData']['structure']
#         logging.info("dominant taut: {}".format(dominant_taut))

#         request = requests.Request(data={'chemical': dominant_taut})
#         response = jchem_rest.mrvToSmiles(request)
#         logging.info("RESPONSE: {}".format(response.content))

#         dominant_taut_smiles = json.loads(response.content)['structure']
#         return dominant_taut_smiles

#     except Exception as e:
#         logging.info("error at getDominateTautomer: {}".format(e))
#         raise e
#     # jchemDataDict.update({taut_obj.name: taut_obj.results})
