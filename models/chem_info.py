# Chemical information model used by CTS workflows
# for building a table on the output pages.



def get_chem_info(workflow_obj):
	data = [
		{'Entered chemical': workflow_obj.chem_struct},
		{'Standardized SMILES': workflow_obj.smiles},
		{'Initial SMILES': workflow_obj.orig_smiles},
		{'IUPAC': workflow_obj.name}, 
		{'Formula': workflow_obj.formula},
		{'CAS #': workflow_obj.cas}, 
		{'Average Mass': workflow_obj.mass},
		{'Monoisotopic Mass': workflow_obj.exactMass}
	]
	return data