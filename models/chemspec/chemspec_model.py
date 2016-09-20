"""
2014-08-13 (np)
"""

import json
from chemaxon_cts import jchem_rest
from chemaxon_cts.jchem_calculator import JchemProperty
import logging
import datetime
from REST import cts_rest


class chemspec(object):
    def __init__(self, run_type, chem_struct, smiles, orig_smiles, name, formula, mass, exact_mass, get_pka, get_taut,
                 get_stereo, pKa_decimals, pKa_pH_lower, pKa_pH_upper, pKa_pH_increment, pH_microspecies,
                 isoelectricPoint_pH_increment, tautomer_maxNoOfStructures, tautomer_pH, stereoisomers_maxNoOfStructures):

        self.jid = jchem_rest.gen_jid()  # timestamp

        self.run_type = run_type

        # Chemical Editor Tab
        self.chem_struct = chem_struct  # SMILE of chemical on 'Chemical Editor' tab
        self.smiles = smiles
        self.orig_smiles = orig_smiles
        self.name = name
        self.formula = formula
        self.mass = "{} g/mol".format(mass)
        self.exact_mass = "{} g/mol".format(exact_mass)

        # Checkboxes:
        self.get_pka = cts_rest.booleanize(get_pka)  # convert 'on'/'off' to bool
        self.get_taut = cts_rest.booleanize(get_taut)
        self.get_stereo = cts_rest.booleanize(get_stereo)

        # Chemical Speciation Tab
        self.pKa_decimals = None
        if pKa_decimals:
            self.pKa_decimals = int(pKa_decimals)
        self.pKa_pH_lower = pKa_pH_lower
        self.pKa_pH_upper = pKa_pH_upper
        self.pKa_pH_increment = pKa_pH_increment
        self.pH_microspecies = pH_microspecies
        self.isoelectricPoint_pH_increment = isoelectricPoint_pH_increment

        self.tautomer_maxNoOfStructures = tautomer_maxNoOfStructures
        self.tautomer_pH = tautomer_pH

        self.stereoisomers_maxNoOfStructures = stereoisomers_maxNoOfStructures

        # Output stuff:
        self.jchemPropObjects = {}
        self.jchemDictResults = {}
        self.speciation_inputs = {}  # for batch mode use


        pkaObj, majorMsObj, isoPtObj, tautObj, stereoObj = None, None, None, None, None

        if self.run_type != 'batch':

            logging.info("Making calls inside chemspec model, single mode...")

            if self.get_pka:
                # make call for pKa:
                pkaObj = JchemProperty.getPropObject('pKa')
                pkaObj.setPostDataValues({
                    "pHLower": self.pKa_pH_lower,
                    "pHUpper": self.pKa_pH_upper,
                    "pHStep": self.pKa_pH_increment,
                })
                pkaObj.makeDataRequest(self.smiles)

                # make call for majorMS:
                majorMsObj = JchemProperty.getPropObject('majorMicrospecies')
                majorMsObj.setPostDataValue('pH', self.pH_microspecies)
                majorMsObj.makeDataRequest(self.smiles)

                # make call for isoPt:
                isoPtObj = JchemProperty.getPropObject('isoelectricPoint')
                isoPtObj.setPostDataValue('pHStep', self.isoelectricPoint_pH_increment)
                isoPtObj.makeDataRequest(self.smiles)

            if self.get_taut:
                tautObj = JchemProperty.getPropObject('tautomerization')
                tautObj.setPostDataValues({
                    "maxStructureCount": self.tautomer_maxNoOfStructures,
                    "pH": self.tautomer_pH,
                    "considerPH": True
                })
                tautObj.makeDataRequest(self.smiles)

            if self.get_stereo:
                # TODO: set values for max stereos!!!
                stereoObj = JchemProperty.getPropObject('stereoisomer')
                stereoObj.setPostDataValue('maxStructureCount', self.stereoisomers_maxNoOfStructures)
                stereoObj.makeDataRequest(self.smiles)

            self.jchemPropObjects = {
                'pKa': pkaObj,
                'majorMicrospecies': majorMsObj,
                'isoelectricPoint': isoPtObj,
                'tautomerization': tautObj,
                'stereoisomers': stereoObj
            }

        else:

            # for batch mode, get inputs but don't get
            # data until output page loads. this is because batch
            # speciation calls are done through nodejs/socket.io
            # using cts_pchemprop_ajax_calls.html

            self.speciation_inputs = {
                'pKa_decimals': pKa_decimals,
                'pKa_decimals': pKa_decimals,
                'pKa_pH_lower': pKa_pH_lower,
                'pKa_pH_upper': pKa_pH_upper,
                'pKa_pH_increment': pKa_pH_increment,
                'pH_microspecies': pH_microspecies,
                'isoelectricPoint_pH_increment': isoelectricPoint_pH_increment
            }
            self.speciation_inputs = json.dumps(self.speciation_inputs)

        self.run_data = {
            'title': "Chemical Speciation Output",
            'jid': self.jid,
            'time': datetime.datetime.strptime(self.jid, '%Y%m%d%H%M%S%f').strftime('%A, %Y-%B-%d %H:%M:%S'),
            'chem_struct': self.chem_struct,
            'smiles': self.smiles,
            'name': self.name,
            'formula': self.formula,
            'mass': self.mass
        }

        for key, value in self.jchemPropObjects.items():
            if value:
                if key == 'pKa':
                    self.jchemDictResults.update({
                        'pka': pkaObj.getMostAcidicPka(),
                        'pkb': pkaObj.getMostBasicPka(),
                        'pka_parent': pkaObj.getParent(),
                        'pka_microspecies': pkaObj.getMicrospecies(),
                        'pka_chartdata': pkaObj.getChartData()
                    })
                elif key == 'majorMicrospecies':
                    self.jchemDictResults.update({key: majorMsObj.getMajorMicrospecies()})
                elif key == 'isoelectricPoint':
                    self.jchemDictResults.update({
                        key: isoPtObj.getIsoelectricPoint(),
                        'isopt_chartdata': isoPtObj.getChartData()
                    })
                elif key == 'tautomerization':
                    self.jchemDictResults.update({'tautomers': tautObj.getTautomers()})
                elif key == 'stereoisomers':
                    self.jchemDictResults.update({key: stereoObj.getStereoisomers()})

        self.run_data.update(self.jchemDictResults)