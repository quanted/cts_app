"""
2014-08-13 (np)
"""
import datetime
import json
import logging
import os
import requests
import pandas as pd
import numpy as np
from rdkit import Chem
from rdkit.Chem import Draw
import base64

from ..generate_timestamp import gen_jid
from ..booleanize import booleanize
from ...cts_api import cts_rest



class chemspec(object):
	def __init__(self, run_type, chem_struct, smiles, orig_smiles, preferredName, name, formula, casrn, cas, dtxsid, mass,
					exactMass, get_pka, get_taut, get_stereo, pKa_decimals, pKa_pH_lower, pKa_pH_upper, pKa_pH_increment, pH_microspecies,
					isoelectricPoint_pH_increment, tautomer_maxNoOfStructures, tautomer_pH, stereoisomers_maxNoOfStructures):

		self.title = "Calculate Chemical Speciation"
		self.jid = gen_jid()
		self.run_type = run_type

		# Chemical Editor Tab
		self.chem_struct = chem_struct  # SMILE of chemical on 'Chemical Editor' tab
		self.smiles = smiles
		self.orig_smiles = orig_smiles

		self.preferredName = preferredName

		self.name = name
		self.formula = formula
		
		self.casrn = casrn  # preferred cas

		self.cas = cas

		self.dtxsid = dtxsid

		self.mass = "{} g/mol".format(mass)
		self.exactMass = "{} g/mol".format(exactMass)

		self.chem_info = {
			'chem_struct': self.chem_struct,
			'smiles': self.smiles,
			'name': self.name,
			'formula': self.formula,
			'exactMass': self.exactMass,
			'mass': self.mass,
			'cas': self.cas,
			'preferredName': self.preferredName,
			'casrn': self.casrn,
			'dtxsid': self.dtxsid
		}

		# Checkboxes:
		self.get_pka = booleanize(get_pka)  # convert 'on'/'off' to bool
		self.get_taut = booleanize(get_taut)
		self.get_stereo = booleanize(get_stereo)

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

		self.run_data = {}
		self.pka_dict_df = None  # dataframe of pka dict

		self.pka_image_html = ""  # <img> of parent with pkas highlighted

		# Output stuff:
		self.speciation_inputs = {}  # for batch mode use
		speciation_results = {}  # speciation prop results
		pkasolver_results = {}
		jchemws_results = {}
		molgpka_results = {}
		measured_results = {}

		if self.run_type != 'batch':
			# Calls cts_rest to get speciation results:
			# speciation_url = os.environ.get('CTS_REST_SERVER') + "/cts/rest/speciation/run"
			post_data = self.__dict__  # payload is class attributes as dict
			post_data['chemical'] = self.smiles
			post_data['service'] = "getSpeciationData"
			post_data['run_type'] = "single"

			speciation_results = cts_rest.getChemicalSpeciationData(post_data)
			speciation_results = json.loads(speciation_results.content)

			jchemws_results = speciation_results["data"].get("data")
			pkasolver_results = speciation_results["data"]["pkasolver"]
			molgpka_results = speciation_results["data"]["molgpka"]
			measured_results = speciation_results["data"]["measured"]


			logging.warning("chemspec_model measured_results: {}".format(measured_results))


			if not "error" in molgpka_results:
				self.pka_image_html = draw_chem_with_pka(molgpka_results["data"]["molgpka_smiles"], molgpka_results["data"]["molgpka_index"])
				self.pka_dict_df = organize_pka(jchemws_results, pkasolver_results, molgpka_results)

		else:
			# Batch speciation calls are done through nodejs/socket.io
			# using cts_pchemprop_requests.html
			self.speciation_inputs = {
				'get_pka': True,
				'pKa_decimals': pKa_decimals,
				'pKa_pH_lower': pKa_pH_lower,
				'pKa_pH_upper': pKa_pH_upper,
				'pKa_pH_increment': pKa_pH_increment,
				'pH_microspecies': pH_microspecies,
				'isoelectricPoint_pH_increment': isoelectricPoint_pH_increment
			}
			self.speciation_inputs = self.speciation_inputs

		self.run_data.update({
			'title': "Chemical Speciation Output",
			'run_type': self.run_type,
			'jid': self.jid,
			'time': datetime.datetime.strptime(self.jid, '%Y%m%d%H%M%S%f').strftime('%A, %Y-%B-%d %H:%M:%S'),
			'chem_struct': self.chem_struct,
			'smiles': self.smiles,
			'name': self.name,
			'formula': self.formula,
			'mass': self.mass,
			'exactMass': self.exactMass
		})
		self.run_data["pkasolver"] = pkasolver_results
		self.run_data["molgpka"] = molgpka_results
		self.run_data["measured"] = measured_results

		self.run_data.update(jchemws_results)


def organize_pka(jchemws_results, pkasolver_results, molgpka_results):
	#chem Axon dataframe	
	ca_df=DictToDF(jchemws_results["pka_dict"])

	#pkasolver dataframe
	solver_df=DictToDF(pkasolver_results["data"]["pka_dict"])

	#MolGpKa -- addional formatting because MolGpKa does not round pka values
	molg_df=DictToDF(molgpka_results["data"]["pka_dict"])
	# RoundMolg(molg_df)

	#combine all dataframes
	full_table=pd.concat([solver_df,molg_df,ca_df],ignore_index=True)
	full_table.insert(0,'Calculator',['pKaSolver','MolGpKa','Chem Axon'])

	#sort dataframe so that pka site (columns) are sorted from lowest average pka to highest
	final=FormatTable(full_table)
	return final


#makes dataframes from pka/atom index dictionaries
def DictToDF(pka_dict):
	#make a dataframe from dictionary-- will result in multiple columns for same atoms (i.e atom_idx=[0,0,5] there will be three columns
	# df=pd.DataFrame([pka_dict.keys()],columns=pka_dict.values()).add_prefix('atom#_')
	df=pd.DataFrame([pka_dict.values()],columns=pka_dict.keys()).add_prefix('atom#_')

	#group columns with the same name (in this case, atom index) and merge the values of those columns using function MergeValues
	df=df.groupby(level=0,axis=1).apply(lambda x:x.apply(MergeValues,axis=1))

	return df


def FormatTable(df):
	col=[]
	col_avg=[]
	for c in df.iloc[:,1:]:
		col.append(c)
		col_val=[]
		for i in df[c].index:
			tmp=df[c][i]

			logging.warning("FormatTable tmp: {}".format(tmp))
			logging.warning("FormatTable tmp type: {}".format(type(tmp)))

			if isinstance(tmp,str):
				logging.warning("FormatTable tmp: {}".format(tmp))
				if ',' in tmp:
					new_tmp=tmp.split(',')
					for n in new_tmp:
						n=round(float(n),2)
						col_val.append(n)
				else:
					n=round(float(tmp),2)
					col_val.append(n)
		col_avg.append(np.mean(col_val))
	d=dict(zip(col,col_avg))
	sort_d=dict(sorted(d.items(),key=lambda item:item[1]))
	col_order=list(sort_d.keys())
	col_order.insert(0,'Calculator')
	df= df.reindex(columns=col_order)
	return df


#merge columns with same names together
def MergeValues(x):
	return ', '.join(x[x.notnull()].astype(str))


def draw_chem_with_pka(smiles, atom_indices):
	"""
	Returns <img> of pkas highlighted where the src is
	a base64 string of the image.

	NOTE: Could be passed through nodeWrapper for a popup
	info table, but probably not needed.
	"""

	mol=Chem.MolFromSmiles(smiles)
	cp=Chem.Mol(mol)

	for i in atom_indices:
		label= "atom#_" + str(i) 
		cp.GetAtomWithIdx(i).SetProp("atomNote",label)

	# d2d = Chem.Draw.rdMolDraw2D.MolDraw2DSVG(350,300)
	d2d = Draw.rdMolDraw2D.MolDraw2DCairo(300,300)
	d2d.drawOptions().setHighlightColour((0.8,0.8,0.8))
	d2d.DrawMolecule(cp,highlightAtoms=atom_indices)
	d2d.FinishDrawing()

	b64_encoded_png = base64.b64encode(d2d.GetDrawingText())
	html_img = '<img src="data:image/png;base64,' + b64_encoded_png.decode('utf-8') + '">'

	return html_img