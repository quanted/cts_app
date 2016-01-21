"""
2014-08-13 (np)
"""

import urllib2
import json
import requests
import chemspec_parameters  # Chemical Speciation parameters
# from REST import rest_funcs
from chemaxon_cts import jchem_rest
from chemaxon_cts.jchem_calculator import JchemProperty as JProp
import logging
# from django.http import HttpRequest
import chemspec_tables
from models.gentrans import data_walks
from django.core.cache import cache
import datetime


class chemspec(object):
    def __init__(self, run_type, chem_struct, smiles, orig_smiles, name, formula, mass, pkaChkbox, tautChkbox, 
                 stereoChkbox, pKa_decimals, pKa_pH_lower, pKa_pH_upper, pKa_pH_increment, pH_microspecies,
                 isoelectricPoint_pH_increment, tautomer_maxNoOfStructures, tautomer_pH, stereoisomers_maxNoOfStructures):

        self.jid = jchem_rest.gen_jid()

        self.run_type = run_type  # hardcoded in pchemprop_output.py

        # Chemical Editor Tab
        self.chem_struct = chem_struct  # SMILE of chemical on 'Chemical Editor' tab
        self.smiles = smiles
        self.orig_smiles = orig_smiles
        self.name = name
        self.formula = formula
        self.mass = mass + ' g/mol'

        # Chemical Speciation Tab
        self.pKa_decimals = int(pKa_decimals)
        self.pKa_pH_lower = pKa_pH_lower
        self.pKa_pH_upper = pKa_pH_upper
        self.pKa_pH_increment = pKa_pH_increment
        self.pH_microspecies = pH_microspecies
        self.isoelectricPoint_pH_increment = isoelectricPoint_pH_increment
        self.tautomer_maxNoOfStructures = tautomer_maxNoOfStructures
        self.tautomer_pH = tautomer_pH
        self.stereoisomers_maxNoOfStructures = stereoisomers_maxNoOfStructures


        # Call jchem server (it's the only one used) to get get server
        # info for the user log file..
        
        
        

        jchemDataDict = {}
        # NOTE: All of this below is just waiting to be turned into a nice loop..
        pkaObj, majorMsObj, isoPtObj, tautObj, stereoObj = None, None, None, None, None

        if pkaChkbox == 'on' or pkaChkbox == True:
            # make call for pKa:
            pkaObj = JProp.getPropObject('pKa')
            pkaObj.setPostDataValues({
                "pHLower": self.pKa_pH_lower,
                "pHUpper": self.pKa_pH_upper,
                "pHStep": self.pKa_pH_increment,
            })
            pkaObj.makeDataRequest(self.chem_struct)
            jchemDataDict.update({pkaObj.name: pkaObj.results})

            # make call for majorMS:
            majorMsObj = JProp.getPropObject('majorMicrospecies')
            majorMsObj.setPostDataValue('pH', self.pH_microspecies)
            majorMsObj.makeDataRequest(self.chem_struct)
            jchemDataDict.update({majorMsObj.name: majorMsObj.results})

            # make call for isoPt:
            isoPtObj = JProp.getPropObject('isoelectricPoint')
            isoPtObj.setPostDataValue('pHStep', self.isoelectricPoint_pH_increment)
            isoPtObj.makeDataRequest(self.chem_struct)
            jchemDataDict.update({isoPtObj.name: isoPtObj.results})

        if tautChkbox == 'on' or tautChkbox == True:
            tautObj = JProp.getPropObject('tautomerization')
            tautObj.setPostDataValues({
                "maxStructureCount": self.tautomer_maxNoOfStructures,
                "pH": self.tautomer_pH,
                "considerPH": True
            })
            tautObj.makeDataRequest(self.chem_struct)
            jchemDataDict.update({tautObj.name: tautObj.results})

        if stereoChkbox == 'on' or stereoChkbox == True:
            stereoObj = JProp.getPropObject('stereoisomer')
            stereoObj.makeDataRequest(self.chem_struct)
            jchemDataDict.update({stereoObj.name: stereoObj.results})

        self.jchemPropObjects = {
            'pKa': pkaObj,
            'majorMicrospecies': majorMsObj,
            'isoelectricPoint': isoPtObj,
            'tautomerization': tautObj,
            'stereoisomers': stereoObj
        }



        # NEW STUFF STARTS HERE (CSV, CACHING, MOSTLY-BACKEND, LESS FRONT) ++++++++++++++++

        run_data = {
            'title': "Chemical Speciation Output",
            'jid': self.jid,
            'time': datetime.datetime.strptime(self.jid, '%Y%m%d%H%M%S%f').strftime('%A, %Y-%B-%d %H:%M:%S'),
            'chem_struct': self.chem_struct,
            'smiles': self.smiles,
            'name': self.name,
            'formula': self.formula,
            'mass': self.mass
        }

        # builds chemspec output json obj for ctsGenerateReport.py
        self.jchemDictResults = {}
        for key, value in self.jchemPropObjects.items():
            if value:
                if key == 'pKa':
                    self.jchemDictResults.update({
                        'pka': pkaObj.getMostAcidicPka(),
                        'pkb': pkaObj.getMostBasicPka(),
                        'pka-parent': pkaObj.getParent(),
                        'pka-microspecies': pkaObj.getMicrospecies()
                        # 'chartData': pkaObj.getChartData()
                    })
                elif key == 'majorMicrospecies':
                    self.jchemDictResults.update({key: majorMsObj.getMajorMicrospecies()})
                elif key == 'isoelectricPoint':
                    self.jchemDictResults.update({
                        'isoelectricPoint': isoPtObj.getIsoelectricPoint()
                        # 'chartData': isoPtObj.getIsoPtChartData()
                    })
                elif key == 'tautomerization':
                    self.jchemDictResults.update({'tautomers': tautObj.getTautomers()})
                elif key == 'stereoisomers':
                    self.jchemDictResults.update({key: stereoObj.getStereoisomers()})

        run_data.update(self.jchemDictResults)
        # cache.set('run_json', json.dumps(run_data), None) # must manually clear after use
        cache.set('chemspec_json', json.dumps(run_data), None) # must manually clear after use