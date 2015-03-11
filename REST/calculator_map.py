
###########################################################
# Herein lies the map to the various calculators' queries #
###########################################################

# TODO: Add chemaxon after these are integrated in

class Calculator:
	"""
	Skeleton class for calculators

	NOTE: molID is recycled, always use "7"
	"""
	def __init__(self, calcName, propMap, urlStruct):
		self.name = calcName
		self.propMap = propMap # expecting list
		self.urlStruct = urlStruct

	def getUrl(self, molID, propKey, method=None):
		if propKey in self.propMap:
			calcProp = self.propMap[propKey]['urlKey']
			if self.name == 'test':
				if method: return self.urlStruct.format(molID, calcProp, method)
				else: return "Error: TEST must have a method in the argument"
			else: 
				return self.urlStruct.format(molID, calcProp)
		else: 
			return "Error: key not found"

	def getResultKey(self, propKey):
		if propKey in self.propMap:
			return self.propMap[propKey]['resultKey']
		else:
			return "Error: key not found"


class TestCalc(Calculator):
	"""
	TEST Calculator
	"""
	def __init__(self):
		urlStruct = "/test/test/calc/{}/{}/{}" # molID, propKey, method
		self.methods = ['hierarchical'] # accounting for one method atm
		propMap = {
			'melting_point': {
				'urlKey': 'meltingPoint',
				'resultKey': 'meltingPointTESTHierarchical',
			},
			'boiling_point': {
				'urlKey': 'boilingPoint',
				'resultKey': 'boilingPointTESTHierarchical'
			},
			'water_sol': {
				'urlKey': 'waterSolubility',
				'resultKey': 'waterSolubilityTESTHierarchical'
			},
			'vapor_press': {
				'urlKey': 'vaporPressure',
				'resultKey': 'vaporPressureTESTHierarchical'
			}
		}
		Calculator.__init__(self, "test", propMap, urlStruct)


class EpiCalc(Calculator):
	"""
	EPI Suite Calculator
	"""
	def __init__(self):
		urlStruct = "/test/epi/calc/{}/{}" # molID, propKey
		# self.methods = None
		propMap = {
			'melting_point': {
				'urlKey': 'meltingPtDegCEstimated',
				'resultKey': 'meltingPtDegCEstimated'
			},
			'boiling_point': {
				'urlKey': 'boilingPtDegCEstimated',
				'resultKey': 'boilingPtDegCEstimated'
			},
			'water_sol': {
				'urlKey': 'waterSolMgLEstimated',
				'resultKey': 'waterSolMgLEstimated'
			},
			'vapor_press': {
				'urlKey': 'vaporPressMmHgEstimated',
				'resultKey': 'vaporPressMmHgEstimated'
			},
			'henrys_law_con': {
				'urlKey': 'henryLcBondAtmM3Mole',
				'resultKey': 'henryLcBondAtmM3Mole'
			},
			'kow_no_ph': {
				'urlKey': 'logKowEstimate',
				'resultKey': 'logKowEstimate'
			},
		}
		Calculator.__init__(self, "epi", propMap, urlStruct)


class MeasuredCalc(Calculator):
	"""
	Measured Data (technically not calculator)
	"""
	def __init__(self):
		urlStruct = "/test/measured/{}/test/{}" # molID, propKey
		# self.methods = None
		propMap = {
			'melting_point': {
				'urlKey': 'meltingPoint',
				'resultKey': 'measuredMeltingPoint',
			},
			'boiling_point': {
				'urlKey': 'boilingPoint',
				'resultKey': 'measuredBoilingPoint'
			},
			'water_sol': {
				'urlKey': 'waterSolubility',
				'resultKey': 'measuredWaterSolubility'
			},
			'vapor_press': {
				'urlKey': 'vaporPressure',
				'resultKey': 'measuredVaporPressure'
			}
		}
		Calculator.__init__(self, "measured", propMap, urlStruct)