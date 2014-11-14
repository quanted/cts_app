import logging
import json
from django.http import HttpRequest
from REST import jchem_rest

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
metabolite_keys = ['smiles', 'accumulation', 'production', 'transmissivity', 'generation']

def traverse(root):

	global metID
	metID += 1
	newDict ={}

	if metID == 1:
		parent = root.keys()[0]
		newDict.update({"id": metID, "name": nodeWrapper(parent, 114, 100), "data": {}, "children": []})
		newDict['data'].update(popupBuilder({"smiles":parent}, metabolite_keys))
		root = root[parent]
	else:
		newDict.update({"id": metID, "name": nodeWrapper(root['smiles'], 114, 100), "data": {}, "children": []})
		# newDict['data'].update({"degradation": root['degradation']})
		newDict['data'].update(popupBuilder(root, metabolite_keys))

	for key, value in root.items():
		if isinstance(value, dict):
			for key2, value2 in root[key].items():
				root2 = root[key][key2]
				if len(root2) > 0: 
					newDict['children'].append(traverse(root2))

	return newDict


def nodeWrapper(smiles, height, width, key=None):
	"""
	Wraps image html tag around
	the molecule's image source

	Inputs: smiles, height, width

	Returns: html of wrapped image
	"""

	# 1. Get image from smiles
	post = {
		"smiles": smiles,
		"height": height,
		"width": width
	}
	request = HttpRequest()
	request.POST = post
	results = jchem_rest.smilesToImage(request)

	# 2. Get imageUrl out of results
	data = json.loads(results.content) # json string --> dict
	imageUrl, imageHeight, imageWidth = '', '', ''
	if 'data' in data:
		root = data['data'][0]['image']
		if 'imageUrl' in root:
			imageUrl = root['imageUrl']
			imageHeight = root['height']
			imageWidth = root['width']

	# 3. Wrap imageUrl with <img>
	html = '<img class="metabolite" '
	if key != None:
		html += 'id="' + key + '" '
	html += 'alt="' + smiles + '" '
	html += 'src="' + imageUrl + '"/>'
	return html


def popupBuilder(root, paramKeys, molKey=None):
	"""
	Wraps molecule data (e.g., formula, iupac, mass, 
	smiles, image) in table

	Inputs 
	root - dictionary of items to wrap in table
	keys - keys to use for building table

	Returns dictionary where html key is 
	the wrapped html and the other keys are
	same as the input keys 
	"""

	# propKeys = ['smiles', 'accumulation', 'production', 'transmissivity', 'generation']
	dataProps = {key: None for key in paramKeys} # metabolite properties 

	html = '<table class="wrapped_molecule">'
	html += '<tr><td rowspan="' + str(len(paramKeys) + 1) + '">' 
	html += nodeWrapper(root['smiles'], 192, 150)
	html += '</td></tr>'
	for key, value in root.items():
		if key in paramKeys:
			dataProps[key] = value
			html += '<tr><td>' + key + '</td>'
			html += '<td>' + str(value) + '</td></tr>'
	html += '</table>'

	dataProps["html"] = html 

	return dataProps 