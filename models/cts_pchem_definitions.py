"""
Definitions for CTS physicochemical properties.
Inspired by creating popups for p-chem table properties.
"""

pchem_defs = {
	"mp": {
		'name': "Melting Point",
		'definition': "The temperature at which a chemical will go from liquid to gaseous phase.",
		'methods': {
			'HC': "Hierarchical Clustering",
			'NN': "Nearest Neighbor",
			'GC': "Group Contribution"
		},
		'cts_props': ['melting_point']
	},
	"bp": {
		'name': "Boiling Point",
		'definition': "The temperature at which a chemical will go from liquid to gaseous phase.",
		'methods': {
			'HC': "Hierarchical Clustering",
			'NN': "Nearest Neighbor",
			'GC': "Group Contribution"
		},
		'cts_props': ['boiling_point']
	},
	"ws": {
		'name': "Water Solubility",
		'definition': "The capacity of a chemical to be dissolved in water. Can be used to understand approximate polarity of a chemical (i.e. more soluble in water = more polar).",
		'methods': {
			'WSKOW': "QSAR model for determining water solubility",
			'WATERNT': "Fragment-based QSAR model for determining water solubility"
		},
		'cts_props': ['water_sol', 'water_sol_ph']
	},
	"vp": {
		'name': "Vapor Pressure",
		'definition': "The force per cubic meter on the base of a column of mercury 1 mm high and with density 13595.1 kg/m^3 (mmHg) that is exerted on a liquid, or solid, when the chemical is evaporating in thermodynamic equilibrium. Used to determine if a chemical is volatile or relatively stable at room temperature.",
		'methods': None,
		'cts_props': ['vapor_press']
	},
	"mdw": {
		'name': "Molecular Diffusivity in Water",
		'definition': "The proportionality constant of molar change between a liquid chemical in question and liquid water due to diffusion. Used to determine how fast a chemical will move in water from a high concentration to a lower concentration.",
		'methods': None,
		'cts_props': ['mol_diss']
	},
	"mda": {
		'name': "Molecular Diffusivity in Air",
		'definition': "The proportionality constant of molar change between a gas chemical in question and air due to diffusion. Used to determine how fast a chemical will move in air from a high concentration to a lower concentration.",
		'methods': None,
		'cts_props': ['mol_diss_air']
	},
	"ic": {
		'name': "Ionization Constant",
		'definition': "The equilibrium constant for a dissociation reaction. Used to measure the strength of an acid.",
		'methods': None,
		'cts_props': ['ion_con']
	},
	"hlc": {
		'name': "Henry's Law Constant",
		'definition': "Proportionality of a dissolved gas to its partial pressure.",
		'methods': None,
		'cts_props': ['henrys_law_con']
	},
	"kow": {
		'name': "Octanol/Water Partition Coefficient",
		'definition': "Proportional relationship of a chemical's tendency to be more soluble in octanol (non-polar) or water (polar). Values above 1 represent more non-polar solvation and values less than 1 represent more polar solvation.",
		'methods': {
			'KLOP': "Method for determining octanol/water partition coefficient using Klopman et al. models (Klopman, G.; Li, Ju-Yun.; Wang, S.; Dimayuga, M.: J.Chem.Inf.Comput.Sci., 1994, 34, 752)",
			'VG': "Method for determining octanol/water partition coefficient derived from Viswanadhan et al. (Viswanadhan, V. N.; Ghose, A. K.; Revankar, G. R.; Robins, R. K., J. Chem. Inf. Comput. Sci., 1989, 29, 163-172)",
			'PHYS': "Method for determining octanol/water partition coefficient based on the PHYSPROP database"
		},
		'cts_props': ['kow_no_ph', 'kow_wph']
	},
	"koc": {
		'name': "Organic Carbon Partition Coefficient",
		'definition': "The ratio of mass of a chemical adsorbed in the soil per unit mass of organic carbon in the soil. Can also be described as the distribution coefficient normalized to the total organic carbon content.",
		'methods': {
				'MCI': "Molecular Connectivity Index method",
				'KOW': "log Kow-based method"
		},
		'cts_props': ['koc']
	},
	"bcf": {
		'name': "Bioconcentration Factor",
		'definition': "The ratio of the concentration of a chemical in an organism due to intake from surrounding water to the concentration of the chemical in the surrounding water.",
		'methods': {
			'REG': "Regression method for determining bioconcentration and bioaccumulation factor",
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
		'definition': "The ratio of the concentration of a chemical in an organism from all intake pathways, including surrounding water and diet, to the concentration of the chemical in the surrounding environment.",
		'methods': {
			'REG': "Regression method for determining bioconcentration and bioaccumulation factor",
			'A-G': "Arnot-Gobas method for determining bioconcentration and bioaccumulation factors"
		},
		'cts_props': ['log_baf']
	}
}

def get_pchem_defs():
	return pchem_defs