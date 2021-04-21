"""
POST objects to test specific CTS workflows.
"""

chemspec_post = {
	"chem_struct":"aspirin",
	"get_pka":"on",
	"pKa_decimals":"2",
	"pKa_pH_lower":"0",
	"pKa_pH_upper":"14",
	"pKa_pH_increment":"0.2",
	"pH_microspecies":"7.0",
	"isoelectricPoint_pH_increment":"0.5",
	"get_taut":"on",
	"tautomer_maxNoOfStructures":"100",
	"tautomer_pH":"7.0",
	"get_stereo":"on",
	"stereoisomers_maxNoOfStructures":"100",
	"chemical":"aspirin",
	"orig_smiles":"CC(=O)OC1=C(C=CC=C1)C(O)=O",
	"smiles":"CC(=O)OC1=C(C=CC=C1)C(O)=O",
	"preferredName":"Aspirin",
	"iupac":"2-(acetyloxy)benzoic acid",
	"formula":"C9H8O4",
	"casrn":"50-78-2",
	"cas":"50-78-2,11126-35-5,11126-37-7,2349-94-2,26914-13-6,98201-60-6",
	"dtxsid":"DTXSID5020108",
	"mass":"180.159",
	"exactmass":"180.042258738"
}

metabolizer_post = {
  "structure": "CCCC",
  "generationLimit": 1,
  "transformationLibraries": [
	"hydrolysis",
	"abiotic_reduction"
  ]
}

envipath_post = {
  "chemical": "CCCC",
  "gen_limit": 1
}

pchem_post = {
  "chemical": "CCC",
  "calc": "chemaxon",
  "prop": "water_sol"
}

def get_post_object(workflow):
	"""
	Returns example POST object for a given workflow.
	"""
	if workflow == "chemspec":
		return chemspec_post

	elif workflow == "metabolizer":
		return metabolizer_post

	elif workflow == "envipath":
		return envipath_post

	else:
		pchem_post["calc"] = workflow 
		return pchem_post
