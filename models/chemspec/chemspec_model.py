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
		self.measured_df = None  # dataframe for measured pka
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

			# TODO: Error handling
			self.measured_df = create_measured_pka_table(measured_results)

			# logging.warning("jchemws_results: {}".format(jchemws_results))
			# logging.warning("pkasolver_results: {}".format(pkasolver_results))
			# logging.warning("molgpka_results: {}".format(molgpka_results))

			valid_pka_results = validate_pka_results(jchemws_results, pkasolver_results, molgpka_results)

			if valid_pka_results:
				self.pka_image_html = draw_chem_with_pka(molgpka_results["data"]["molgpka_smiles"], molgpka_results["data"]["molgpka_index"])
				# self.pka_dict_df = organize_pka(jchemws_results, pkasolver_results, molgpka_results)
				self.pka_dict_df = FormatTableUpdated(jchemws_results, pkasolver_results, molgpka_results)

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


def create_measured_pka_table(measured_results):
	"""
	Creates dataframe for measured pka table.
	"""
	# NOTE: Ensure error handling is happening before created_measured_pka_table is called:
	
	measured_dict = dict(measured_results["data"])
	measured_dict["Calculator"] = "Measured"

	measured_dict["Full_Reference"] = create_full_ref_link(measured_dict)

	pka_vals = {k: round(v, 2) for k, v in measured_dict.items() if k.startswith("pKa_")}
	pka_headers = ["pKa_{}".format(i + 1) for i in range(len(pka_vals))]

	all_headers = ["Calculator"] + pka_headers + ['InText','DOI','Full_Reference']

	measured_df = pd.DataFrame([measured_dict], columns=all_headers)

	return measured_df


def create_full_ref_link(measured_dict):
	"""
	Full ref link that will open refs page with InText in param.
	"""
	full_ref = measured_dict.get("Full_Reference")
	intext = measured_dict.get("InText")

	if not intext or not isinstance(intext, str):
		return "N/A"

	wrapped_full_ref = f"<a href='/cts/about/measured-pka-refs?search={intext}' target='_blank'>Click for ref</a>"

	return wrapped_full_ref


def validate_pka_results(jchemws_results, pkasolver_results, molgpka_results):
	"""
	Validates pka results for comparison table.
	"""
	if "error" in molgpka_results or "error" in pkasolver_results or "error" in jchemws_results:
		return False
	if not jchemws_results.get("pka_dict") or len(jchemws_results["pka_dict"]) < 1:
		return False
	if not pkasolver_results["data"].get("pka_dict") or len(pkasolver_results["data"]["pka_dict"]) < 1:
		return False
	if not molgpka_results["data"].get("pka_dict") or len(molgpka_results["data"]["pka_dict"]) < 1:
		return False
	return True


def organize_pka(jchemws_results, pkasolver_results, molgpka_results):

	#chem Axon dataframe	
	ca_df=DictToDF(jchemws_results["pka_dict"])

	#pkasolver dataframe
	solver_df=DictToDF(pkasolver_results["data"]["pka_dict"])

	#MolGpKa -- addional formatting because MolGpKa does not round pka values
	molg_df=DictToDF(molgpka_results["data"]["pka_dict"])
	# RoundMolg(molg_df)

	print("ca_df: {}".format(ca_df))	
	print("solver_df: {}".format(solver_df))
	print("molg_df: {}".format(molg_df))


	#combine all dataframes
	full_table=pd.concat([solver_df,molg_df,ca_df],ignore_index=True)
	full_table.insert(0,'Calculator',['pKaSolver','MolGpKa','ChemAxon'])

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
			if isinstance(tmp,str):
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

	try:

		for i in atom_indices:
			label= "atom#_" + str(i)
			cp.GetAtomWithIdx(i).SetProp("atomNote",label)

		d2d = Draw.rdMolDraw2D.MolDraw2DCairo(300,300)
		d2d.drawOptions().setHighlightColour((0.8,0.8,0.8))
		d2d.DrawMolecule(cp,highlightAtoms=atom_indices)
		d2d.FinishDrawing()

	except Exception as e:
		logging.error("chemspec_model draw_chem_with_pka exception: {}".format(e))
		return ""

	b64_encoded_png = base64.b64encode(d2d.GetDrawingText())
	html_img = '<img src="data:image/png;base64,' + b64_encoded_png.decode('utf-8') + '">'

	return html_img







def MakeMultilevelHeader(dict,tuple_lst):
	#make a multi level index using the tuples where level 0 is the category and level 1 is the atom index
	cols=pd.MultiIndex.from_tuples(tuple_lst)

	#make dataframe with pka values and multilevel column headers (transpose so that multilevel lables are column headers and not index
	df=pd.DataFrame([dict.values()],columns=cols)
	return df


def SortLow2High(df):
	col_avg=[]
	col_idx=[]
	#look at only pka data (removes calculator name col and acid/base row)
	for c in df.iloc[1:4,1:]:
		col_idx.append(c)
		#average of column
		col_val=round(df.iloc[1:4,c].mean(),2)
		col_avg.append(col_val)
	#make dictionary with column index (key) and column average
	d=dict(zip(col_idx,col_avg))
	#sort sort (low to high) columns based on value, if value is the same then sort by key
	sort_d=dict(sorted(d.items(), key=lambda kv: (kv[1], kv[0])))
	col_order=list(sort_d.keys())
	#reindex dataframe so with new column order
	new=df.reindex(columns=col_order)
	#make the last row (atom#_) row the header
	new.rename(columns=new.iloc[4],inplace=True)
	#remove the last row
	new.drop(new.index[4], inplace = True)
	#add calculator column
	new.insert(0,'Calculator',['','Chem Axon','MolGpKa','pKaSolver'])
	return new


def handle_speciation_data(speciation_results):
	"""
	Parses data into objects for creating table.
	"""
	ca_dict = {}
	ca_tuples = []

	# Extract lists for comparison
	pka_list = speciation_results.get('pka', [])
	pkb_list = speciation_results.get('pkb', [])

	pka_list = [round(x, 2) for x in pka_list]
	pkb_list = [round(x, 2) for x in pkb_list]


	print("pka_list: {}".format(pka_list))
	print("pkb_list: {}".format(pkb_list))
	
	# Process each atom number and value in pka_dict
	for atom_num_str, value in speciation_results.get('pka_dict', {}).items():


		print("atom_num_str: {}".format(atom_num_str))

		print("value: {}".format(value))

		atom_num = int(atom_num_str)
		
		# Check if value appears in pka list (acid)
		if value in pka_list:
			key = ("acid", atom_num)
			ca_dict[key] = value
			ca_tuples.append(key)
			
		# Check if value appears in pkb list (base)
		elif value in pkb_list:
			key = ("base", atom_num)
			ca_dict[key] = value
			ca_tuples.append(key)

	return ca_dict, ca_tuples


# def FormatTableUpdated(smiles, speciation_results):
def FormatTableUpdated(jchemws_results, pkasolver_results, molgpka_results):

	ca_dict, ca_tuples = handle_speciation_data(jchemws_results)

	# print("ca_dict: {}".format(ca_dict))
	# print("ca_tuples: {}".format(ca_tuples))

	ca_df = MakeMultilevelHeader(ca_dict,ca_tuples)

	# print("ca_df: {}".format(ca_df))

	mg_dict = molgpka_results["data"].get("mg_dict", {})
	mg_tuples = molgpka_results["data"].get("mg_tuples", [])

	mg_dict = {eval(k): v for k, v in mg_dict.items()}  # convert keys to tuples
	mg_tuples = [eval(x) for x in mg_tuples]  # convert items to tuples

	solver_dict = pkasolver_results["data"].get("pkasolver_dict", {})
	
	solver_dict = {float(k): v for k, v in solver_dict.items()}

	# print(">>> mg_dict: {}".format(mg_dict))
	# print("mg_tuples: {}".format(mg_tuples))
	# print("solver_dict: {}".format(solver_dict))

	# TODO: Convert mg and solver result tuples from string to actual tuples.
	
	####Molgpka
	#make dataframe from dictionary and tuples; tuples are column multilevel headers
	molg_df=MakeMultilevelHeader(mg_dict,mg_tuples)
	
	####pkasolver
	#make a dataframe from dictionary 
	solver_df=pd.DataFrame([solver_dict.keys()],columns=solver_dict.values())
	
	#combine pka values with the same atom index
	solver_df=solver_df.groupby(level=0,axis=1).apply(lambda x:x.apply(list,axis=1))

	# logging.warning("solver_df: {}".format(solver_df))
	# logging.warning("ca_df: {}".format(ca_df))
	# logging.warning("molg_df: {}".format(molg_df))

	
	#concat chem axon and molg pka using multilevel index
	both=pd.concat([ca_df,molg_df],ignore_index=True)
	
	#grab categrory information from level 0 of multilevel indexing,make it a new row
	both.loc[len(both)]=both.columns.get_level_values(0)
	
	#drop top level in multilevelindexing
	both.columns=both.columns.droplevel()
	
	#group pka preds for a particular site in chemaxon/molg df
	test=both.groupby(level=0,axis=1).apply(lambda x:x.apply(list,axis=1))
	
	#handle cases where pkasolver has more or fewer sites than molg/chemaxon
	#note: comparing num of pka preds/site for pkasolver and molg because I doubt chemaxon will predict >1 pka/site
	for c in solver_df.columns:
		v=solver_df[c][0]
		if c in test.columns:
			ca=test.loc[0,c]
			mg=test.loc[1,c]
			#if there are more pkasolver preds for a particular site than preds from molg
			if len(v) > len(mg):       
				for i in range(len(mg)):
					if np.isnan(ca[i])==False:
						#get average pka for molg and chemaxon at a particular site/category
						avg=((ca[i]+mg[i])/len(mg))
					else:
						avg=mg[i]
					#sort solver preds based on how close (smallest diff) pred is to avg
					tmp=sorted(v,key=lambda x: abs(avg-x)) 
					solver_df[c][0]=tmp
					
			#if there are more molg preds for particular site than preds from pkasolver
			#just concat because all values will be low --> high
			else:
				all=pd.concat([test,solver_df],ignore_index=True)
		else:
			all=pd.concat([test,solver_df],ignore_index=True)
  
	#add 'Calculators' column
	all.insert(0,'Calculator',['Chem Axon','MolGpKa',' ','pKaSolver'])
	
	#sort by calculator so that acid/base row is at the top
	all.sort_values(by='Calculator',ignore_index=True,inplace=True)

	 #seperate out listed values from pkasolver  
	for c in all.iloc[1:,1:].columns:
		for i in all.iloc[1:,1:].index:
			x=all[c][i]
			if np.isnan(x).all()==True:
				all.loc[i,c]=np.nan
			elif len(x) > 1:
					all.loc[i,[c,str(c)]]=x[0],x[1] #duplicate columns names, must store one as a string and one as int
			else:
					all.loc[i,c]=x[0]
	#separate out type
	for c in all.iloc[1:,1:].columns:
		for t in all.iloc[:1,:1].index:
			x=all[c][t]
			if isinstance(x, (str,float)):
				break
			elif len(x) > 1:
			   all.loc[t,[c,str(c)]]=x[0],x[1] #duplicate columns names, must store one as a string and one as int
			else:
					all.loc[t,c]=x[0]
			
	#add 'atom#_' prefix
	all=all.iloc[:,1:].add_prefix('atom#_')
	
	#add 'Calculators' column
	all.insert(0,'Calculator',[' ','Chem Axon','MolGpKa','pKaSolver'])
	
	## temporary formatting for column sorting 
	## needed because of duplicate column names
	#add atom header as a row
	all.loc[len(all)]=all.columns.get_level_values(0)
	
	#rename columns as 0,1,2,3...n
	all.columns=range(all.columns.size)

	#sort table for lowest avg. pka to highest avg. pka
	table=SortLow2High(all)

	print("Updated pka comparison table: {}".format(table))

	return table