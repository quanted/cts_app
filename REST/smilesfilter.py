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

    logging.info("inside check mass function..")

    request = requests.Request(data = { 'smiles': smiles })
    # request.data = { 'smiles': structure }

    logging.info("checking mass..")

    try:
        response = jchem_rest.getMass(request) # get mass from jchem ws
        json_obj = json.loads(response.content)
    except Exception as e:
        logging.warning("!!! Error in checkMass() {} !!!".format(e))
        raise e

    logging.info("mass response data: {}".format(response.content))
    
    struct_mass = json_obj['data'][0]['mass']

    logging.info("structure's mass: {}".format(struct_mass))

    if struct_mass < 1500  and struct_mass > 0:
        return True
    else:
        return False


def clearStereos(smiles):
    """
    clears stereoisomers from smiles
    """
    request = requests.Request(data={'smiles':smiles})
    try:
        response = jchem_rest.clearStereo(request)
        filtered_smiles = json.loads(response.content)['results'] # get stereoless structure
    except Exception as e:
        logging.warning("!!! Error in clearStereos() {} !!!".format(e))
        raise e
    return filtered_smiles


def transformSMILES(smiles):
    """
    [N+](=O)[O-] >> N(=O)=O
    """
    request = requests.Request(data={'smiles':smiles})
    try:
        response = jchem_rest.transform(request)
        logging.info("transform response: {}".format(response.content))
        filtered_smiles = json.loads(response.content)['results']
    except Exception as e:
        logging.warning("!!! Error in transformSMILES() {} !!!".format(e))
        raise e
    return filtered_smiles


def parseSmilesByCalculator(structure, calculator):
    """
    Calculator-dependent SMILES filtering!
    """
    from chemaxon_cts import jchem_rest

    logging.info("Parsing SMILES by calculator..")
    filtered_smiles = '' # do i need to initialize up here???

    #1. check structure mass..
    if calculator == 'epi' or calculator == 'test':
        logging.info("checking mass for: {}...".format(structure))
        if not checkMass(structure):
            logging.info("Structure too large, must be < 1500 g/mol..")
            raise "Structure too large, must be < 1500 g/mol.."

    #2-3. clear stereos from structure, transform [N+](=O)[O-] >> N(=O)=O..
    if calculator == 'epi' or calculator == 'sparc':

        logging.info("clearing stereoisomers from smiles..")

        try:
            # clear stereoisomers:
            filtered_smiles = clearStereos(structure)
            logging.info("stereos cleared: {}".format(filtered_smiles))

            # transform structure:
            filtered_smiles = str(filtered_smiles[-1])
            filtered_smiles = str(transformSMILES(filtered_smiles)[-1])
            logging.info("structure transformed..")
        except Exception as e:
            logging.warning("!!! Error in parseSmilesByCalculator() {} !!!".format(e))
            raise e

    return filtered_smiles