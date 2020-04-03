"""
Current list of user-level CTS error messages.
See /cts/about/errors page for table.
"""

cts_errors = [
	{
		'index': 1,
		'name': "calc_smiles_filter_error",
		'message': "Cannot filter SMILES for [calc name] data",
		'description': "An error occurred during the chemical information request routine.",
		'suggestions': "Please make sure that the chemical fits with the types of chemicals that CTS can accept as described in the Intended Use section. It may also help to try a different identifier. CTS accepts names, SMILES strings, CAS #s, and drawn structures. "
	},
	{
		'index': 2,
		'name': "smiles_filter_error",
		'message': "Cannot process chemical",
		'description': "Error message that's returned if the SMILES standardization routine produces an error.",
		'suggestions': "Please make sure that the chemical fits with the types of chemicals that CTS can accept as described in the Intended Use section. It may also help to try a different identifier. CTS accepts names, SMILES strings, CAS #s, and drawn structures. "
	},
	{
		'index': 3,
		'name': "calc_general_error",
		'message': "Cannot reach [calc name] calculator",
		'description': "An unexpected error occurred when trying to get data from a calculator server (e.g., server is down, or something is wrong with server internally).",
		'suggestions': "Please try the request again later. "
	},
	{
		'index': 4,
		'name': "salt_mixtures_error",
		'message': "Chemical cannot be salt or mixture",
		'description': "Returned if the entered chemical is a salt or mixture.",
		'suggestions': "The entered chemical is not supported by CTS. Please enter a different chemical."
	},
	{
		'index': 5,
		'name': "metals_error",
		'message': "Chemical cannot contain metals",
		'description': "Error is raised if chemical contains any metals. CTS does not accept chemicals with metals. (see 'Intended Use' in the About section)",
		'suggestions': "The entered chemical is not supported by CTS. Please enter a different chemical."
	},
	{
		'index': 6,
		'name': "carbon_check_error",
		'message': "CTS only accepts organic chemicals",
		'description': "This error is returned if the chemical does not contain carbon.",
		'suggestions': "The entered chemical is not supported by CTS. Please enter a different chemical."
	},
	{
		'index': 7,
		'name': "chem_type_error",
		'message': "error getting chemical type",
		'description': "Is returned if CTS is unable to get chemical type of user-entered chemical from ChemAxon.",
		'suggestions': "Please try a different identifier. CTS accepts names, SMILES strings, CAS #s, and drawn structures. If none of these options work, CTS may not support the chemical you are looking for. Contact us  at cts@epa.gov with your request information if you believe CTS supports your chemical but you are still seeing an error."
	},
	{
		'index': 8,
		'name': "cts_rest_general_error",
		'message': "Error requesting data from [calc name]",
		'description': "Top-level exception for CTS REST requests. If an unexpected issue occurs that's not caught by specific error handling, this error is thrown. (API-specific error)",
		'suggestions': "Please contact us at cts@epa.gov with your request information so we can reproduce and examine this unknown error."
	},
	{
		'index': 9,
		'name': "chem_info_error",
		'message': "Error validating chemical, Cannot validate chemical",
		'description': "An error occurred during the chemical information request routine.",
		'suggestions': "Please make sure that the chemical fits with the types of chemicals that CTS can accept as described in the Intended Use section. It may also help to try a different identifier. CTS accepts names, SMILES strings, CAS #s, and drawn structures."
	},
	{
		'index': 10,
		'name': "data_not_available",
		'message': "N/A",
		'description': "The calculator request was successful, but there wasn't any available data for the given chemical and property. For estimated values, the chemical is outside of the applicability domain of the calculator. For measured values, there is no measured data for the property in the PHYSPROP database.",
		'suggestions': "It may help to try a different calculator that provides this property when available."
	},
	{
		'index': 11,
		'name': "no_pka_error",
		'message': "none",
		'description': "Message raised in the ionization constant calculation of the physicochemical properties table. Message indicates that the calculation was successful and the calculator shows no ionization constants from pH 0-14.",
		'suggestions': "If an ionization constant is expected between pH 0 and 14, it may help to try a different calculator that provides this property when available."
	},
	{
		'index': 12,
		'name': "speciation_post_error",
		'message': "speciation POST needed",
		'description': "Returned if POST is incorrect when making speciation request. (API-specific error)",
		'suggestions': "Please correct the format and/or data in the POST request to comply with our API format."
	},
	{
		'index': 13,
		'name': "chem_size_error",
		'message': "Structure too large, must be < 1500 g/mol",
		'description': "Error is raised if chemical's molecular weight is greater than 1500 g/mol. CTS cannot process chemicals with a molecular weight over 1500 g/mol.",
		'suggestions': "The entered chemical is not supported by CTS. Please enter a different chemical."
	}
]