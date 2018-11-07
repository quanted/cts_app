"""
Current list of user-level CTS error messages.
See /cts/about/errors page for table.
"""

cts_errors = [
	{
		'index': 1,
		'name': "chem_size_error",
		'message': "Structure too large, must be < 1500 g/mol",
		'description': "Is raised if chemical is greater than 1500 g/mol."
	},
	{
		'index': 2,
		'name': "metals_error",
		'message': "Chemical cannot contain metals",
		'description': "Returns error if chemical contains any metals (see 'Intended Use' in the About section)."
	},
	{
		'index': 3,
		'name': "smiles_filter_error",
		'message': "Cannot process chemical",
		'description': "Error message that's returned if something goes wrong when standardizing the SMILES."
	},
	{
		'index': 4,
		'name': "chem_info_error",
		'message': "Error validating chemical, Cannot validate chemical",
		'description': "An unexpected error occurred during the chemical information request routine."
	},
	{
		'index': 5,
		'name': "calc_smiles_filter_error",
		'message': "Cannot filter SMILES for [calc name] data",
		'description': "Is returned when an error occurred during the chemical information request routine."
	},
	{
		'index': 6,
		'name': "speciation_post_error",
		'message': "speciation POST needed",
		'description': "Returned if POST is incorrect when making speciation request."
	},
	{
		'index': 7,
		'name': "calc_general_error",
		'message': "Cannot reach [calc name] calculator",
		'description': "An unexpected error occurred when trying to get data from a calculator server (e.g., server is down, or something is wrong with server internally)."
	},
	{
		'index': 8,
		'name': "chem_type_error",
		'message': "error getting chemical type",
		'description': "Is returned if CTS is unable to get chemical type of user-entered chemical from ChemAxon."
	},
	{
		'index': 9,
		'name': "cts_rest_general_error",
		'message': "Error requesting data from [calc name]",
		'description': "Top-level exception for CTS REST requests. If an unexpected issue occurs that's not caught by specific error handling, this error is thrown."
	},
	{
		'index': 10,
		'name': "data_not_available",
		'message': "N/A",
		'description': "The calculator request was successful, but there wasn't any available data for the given chemical."
	},
	{
		'index': 11,
		'name': "salt_mixtures_error",
		'message': "Chemical cannot contain be salt or mixture",
		'description': "This error is returned if the chemical contains a salt or mixture."
	}
]