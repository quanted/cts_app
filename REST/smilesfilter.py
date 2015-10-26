__author__ = 'KWOLFE'

from chemaxon_cts import jchem_rest
import requests
import logging
import json
from chemaxon_cts.jchem_calculator import JchemProperty as JProp


max_weight = 1500 # max weight [g/mol] for epi, test, and sparc


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
        filtered_smiles = json.loads(response.content)['results'][0] # picks out smiles from efs???
        logging.info("NEW SMILES: {}".format(filtered_smiles))
        return filtered_smiles
    except Exception as e:
        logging.info("> error in filterSMILES: {}".format(e))
        raise e
