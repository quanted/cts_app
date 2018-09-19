"""
Definitions for CTS physicochemical properties.
Inspired by creating popups for p-chem table properties.
"""

pchem_defs = {
	"mp": {
		'name': "Melting Point",
		'definition': "The temperature at which a chemical changes from liquid to gaseous phase.",
		'methods': {
			'HC': "Hierarchical Clustering",
			'NN': "Nearest Neighbor",
			'GC': "Group Contribution"
		},
		'cts_props': ['melting_point']
	},
	"bp": {
		'name': "Boiling Point",
		'definition': "The temperature at which a chemical changes from liquid to gaseous phase.",
		'methods': {
			'HC': "Hierarchical Clustering",
			'NN': "Nearest Neighbor",
			'GC': "Group Contribution"
		},
		'cts_props': ['boiling_point']
	},
	"ws": {
		'name': "Water Solubility",
		'definition': "The maximum concentration of a chemical compound which can result when it is dissolved in water. For solids, a correction factor has been applied to convert estimated supercooled values to the vapor pressure of the solid.",
		'methods': {
			'WSKOW': "QSAR model for determining water solubility",
			'WATERNT': "Fragment-based QSAR model for determining water solubility"
		},
		'cts_props': ['water_sol']
	},
	"vp": {
		'name': "Vapor Pressure",
		'definition': "The force per unit area exerted by a vapor in an equilibrium state with its pure solid, liquid, or solution at a given temperature. Vapor pressure is a measure of a substance's propensity to evaporate. For solids, a correction factor has been applied to convert estimated supercooled values to the vapor pressure of the solid.",
		'methods': None,
		'cts_props': ['vapor_press']
	},
	"mdw": {
		'name': "Molecular Diffusivity in Water",
		'definition': "The proportionality constant of molar flux due to molecular diffusion in water and the concentration gradient of the chemical in water. Molecular diffusion in water is the process in which solutes are transported at the microscopic level as the result of their spontaneous movement from regions of higher concentrations to regions of lower concentrations.",
		'methods': None,
		'cts_props': ['mol_diss']
	},
	"mda": {
		'name': "Molecular Diffusivity in Air",
		'definition': "The proportionality constant of molar flux due to molecular diffusion in air and the concentration gradient of the chemical in air. Molecular diffusion in air is the process in which gases are transported at the microscopic level as the result of their spontaneous movement from regions of higher concentrations to regions of lower concentrations.",
		'methods': None,
		'cts_props': ['mol_diss_air']
	},
	"ic": {
		'name': "Ionization Constant",
		'definition': "The equilibrium constant for an acid or base dissocation reaction. The constant provides a measure of the strength of an acid or base.",
		'methods': None,
		'cts_props': ['ion_con']
	},
	"hlc": {
		'name': "Henry's Law Constant",
		'definition': "The ratio of the concentration of a compound in air to the concentration of the compound in water under equilibrium conditions.",
		'methods': None,
		'cts_props': ['henrys_law_con']
	},
	"kow": {
		'name': "Octanol/Water Partition Coefficient",
		'definition': "The ratio of the concentration of a compound inn n-octanol (a non-polar solvent) to its concentration in water (a polar solvent). The higher the Kow, the more non-polar the compound.",
		'methods': {
			'KLOP': "Method for determining Kow using Klopman et al. models (Klopman, G.; Li, Ju-Yun.; Wang, S.; Dimayuga, M.: J.Chem.Inf.Comput.Sci., 1994, 34, 752)",
			'VG': "Method for determining Kow derived from Viswanadhan et al. (Viswanadhan, V. N.; Ghose, A. K.; Revankar, G. R.; Robins, R. K., J. Chem. Inf. Comput. Sci., 1989, 29, 163-172)",
			'PHYS': "Method for determining Kow based on the VG model with the PHYSPROP database as a training set"
		},
		'cts_props': ['kow_no_ph']
	},
	"koc": {
		'name': "Organic Carbon Partition Coefficient",
		'definition': "The ratio of mass of a chemical adsorbed to soil organic carbon to the concentration of the chemical in water under equilibrium conditions. Can also be described as the soil-water distribution coefficient (Koc) normalized to the total organic carbon content of the soil.",
		'methods': {
				'MCI': "Molecular Connectivity Index method",
				'KOW': "log Kow-based method"
		},
		'cts_props': ['koc']
	},
	"bcf": {
		'name': "Bioconcentration Factor",
		'definition': "The ratio of the concentration of a chemical in an organism due to uptake from surrounding water to the concentration of the chemical in the surrounding water.",
		'methods': {
			'REG': "Regression method for determining bioconcentration factors",
			'A-G': "Arnot-Gobas method for determining bioconcentration and bioaccumulation factors",
			'SM': "Single Model",
			'HC': "Hierarchical Clustering",
			'NN': "Nearest Neighbor",
			'GC': "Group Contribution"
		},
		'cts_props': ['log_bcf']
	},
	"baf": {
		'name': "Bioaccumulation Factor",
		'definition': "The ratio of the concentration of a chemical in an organism from all uptake pathways, including respiration, dermal uptake, and diet, to the concentration of the chemical in the surrounding environment.",
		'methods': {
			'A-G': "Arnot-Gobas method for determining bioconcentration and bioaccumulation factors"
		},
		'cts_props': ['log_baf']
	},
	"d_ow": {
		'name': "Octanol/Water Distribution Coefficient",
		'definition': "The ratio of the concentration of a compound in n-octanol (a non-polar solvent) to its concentration in water (a polar solvent) at a user-specified pH value. The higher the d_ow , the more non-polar the compound.",
		'methods': {
			'KLOP': "Method for determining d_ow using Klopman et al. models (Klopman, G.; Li, Ju-Yun.; Wang, S.; Dimayuga, M.: J.Chem.Inf.Comput.Sci., 1994, 34, 752)",
			'VG': "Method for determining d_ow derived from Viswanadhan et al. (Viswanadhan, V. N.; Ghose, A. K.; Revankar, G. R.; Robins, R. K., J. Chem. Inf. Comput. Sci., 1989, 29, 163-172)",
			'PHYS': "Method for determining d_ow based on the VG model with the PHYSPROP database as a training set"
		},
		'cts_props': ['kow_wph']
	},
	"wsph": {
		'name': "Water Solubility",
		'definition': "The maximum concentration of a chemical compound which can result when it is dissolved in water, adjusted to a user-specified pH. For solids, a correction factor has been applied to convert estimated supercooled values to the vapor pressure of the solid.",
		'methods': {
			'WSKOW': "QSAR model for determining water solubility",
			'WATERNT': "Fragment-based QSAR model for determining water solubility",
			'HC': "Hierarchical Clustering",
			'NN': "Nearest Neighbor",
			'GC': "Group Contribution"
		},
		'cts_props': ['water_sol_ph']
	}
}

def get_pchem_defs():
	return pchem_defs