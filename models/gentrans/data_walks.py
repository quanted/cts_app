import logging
import json

"""
10-31-14 (np)
Recursively walks n-nested dictionary
in json format and restructures the data to
comply with the jquery flow chart library
used: jit (thejit.org)
"""

def recursive(jsonStr):
	jsonDict = json.loads(jsonStr)
	root = jsonDict['results']
	reDict = {}
	parent = root.keys()[0]
	reDict.update(traverse(root))
	return json.dumps(reDict)


metID = 0 # unique id for each node


def traverse(root):
	global metID
	metID += 1
	newDict ={}

	logging.warning(root.keys())

	if metID == 1:
		parent = root.keys()[0]
		# newDict.update({"id": metID, "name": parent, "data": {}, "children": []})
		newDict.update({"id": metID, "name": metID, "data": {}, "children": []})
		root = root[parent]
	else:
		# newDict.update({"id": metID, "name": root['smiles'], "data": {}, "children": []})
		newDict.update({"id": metID, "name": metID, "data": {}, "children": []})
		newDict['data'].update({"degradation": root['degradation']})

	for key, value in root.items():
		if isinstance(value, dict):
			for key2, value2 in root[key].items():
				root2 = root[key][key2]
				if len(root2) > 0: 
					newDict['children'].append(traverse(root2))

	return newDict