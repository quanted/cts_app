__author__ = 'KWOLFE'

from chemaxon_cts import jchem_rest
import requests
import logging
import json
from chemaxon_cts.jchem_calculator import JchemProperty as JProp


max_weight = 1500 # max weight [g/mol] for epi, test, and sparc


def is_valid_smiles(smiles):

    excludestring = {".","[Ag]","[Al]","[Au]","[As]","[As+","[B]","[B-]","[Br-]","[Ca]",
                        "[Ca+","[Cl-]","[Co]","[Co+","[Fe]","[Fe+","[Hg]","[K]","[K+","[Li]",
                        "[Li+","[Mg]","[Mg+","[Na]","[Na+","[Pb]","[Pb2+]","[Pb+","[Pt]",
                        "[Sc]","[Si]","[Si+","[SiH]","[Sn]","[W]"}

    return_val = {
            "valid" : False,
            "smiles": smiles,
            "processedsmiles" : ""
    }

    if any(x in smiles for x in excludestring):
        return return_val

    try:
        processed_smiles = filterSMILES(smiles)
    except Exception as e:
        logging.warning("!!! Error in smilesfilter {} !!!".format(e))
        raise "smiles filter exception, possibly invalid smiles..."
            
    return_val["valid"] = True
    return_val["processedsmiles"] = processed_smiles

    return return_val


def filterSMILES(smiles):
    """
    calculator-independent SMILES processing.
    uses jchem web services through jchem_rest
    """
    
    request = requests.Request(data={'smiles': smiles}) # wrap smiles in http request
    response = jchem_rest.filterSMILES(request)
    logging.info("FILTER RESPONSE: {}".format(response.content))

    try:
        filtered_smiles = json.loads(response.content)['results'][0] # picks out smiles from efs???
        logging.info("NEW SMILES: {}".format(filtered_smiles))
        return filtered_smiles
    except Exception as e:
        logging.info("> error in filterSMILES: {}".format(e))
        raise e


def checkMass(smiles):
    """
    returns true is smiles mass is less
    than 1500 g/mol
    """
    request = requests.Request()
    request.data = { 'smiles': structure }

    try:
        response = jchem_rest.getMass(request) # get mass from jchem ws
        json_obj = json.loads(response.content)
    except Exception as e:
        logging.warning("!!! Error in checkMass() {} !!!".format(e))
        raise e
    
    struct_mass = json_obj['data'][0]['mass']
    if struct_mass < 1500  and struct_mass > 0:
        return True
    else:
        return False


def clearStereos(smiles):
    """
    clears stereoisomers from smiles
    """
    request = requests.Request()
    request.data = { 'smiles': structure }

    try:
        response = jchem_rest.clearStereo(request)
        request.data = { 'chemical': response.content } # structure in mrv format

        response = jchem_rest.convertToSMILES(request) # mrv >> smiles
        filtered_smiles = json.loads(response.content)['structure'] # get stereoless structure
    except Exception as e:
        logging.warning("!!! Error in clearStereos() {} !!!".format(e))
        raise e

    return filtered_smiles


def transformSMILES(smiles):
    """
    [N+](=O)[O-] >> N(=O)=O
    """
    request = requests.Request()
    request.data = { 'smiles': filtered_smiles }

    try:
        response = jchem_rest.transform(request)

        request.data = { 'chemical': filtered_smiles }
        response = jchem_rest.convertToSMILES(request)
        filtered_smiles = json.loads(response.content)['structure']
    except Exception as e:
        logging.warning("!!! Error in transformSMILES() {} !!!".format(e))
        raise e

    return filtered_smiles


def parseSmilesByCalculator(structure, calculator):
    """
    EPI Suite dependent SMILES filtering!
    """
    from chemaxon_cts import jchem_rest

    #1. check structure mass..
    if calculator == 'epi' or calculator == 'test':
        if not checkMass(structure):
            raise "Structure too large, must be < 1500 g/mol.."

    #2-3. clear stereos from structure, transform [N+](=O)[O-] >> N(=O)=O..
    if calculator == 'epi' or calculator == 'sparc':
        try:
            filtered_smiles = clearStereos(structure)
            filtered_smiles = transformSMILES(structure)
        except Exception as e:
            logging.warning("!!! Error in parseSmilesByCalculator() {} !!!".format(e))
            raise e

    logging.info(">>> FILTERED SMILES: {}".format(filtered_smiles))

    return filtered_smiles