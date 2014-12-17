import logging
import json
from django.http import HttpRequest
from REST import jchem_rest
from django.utils.encoding import smart_text
import os
from django.template import Context, Template, defaultfilters

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
	"""
	For gentrans model output
	"""

	global metID
	metID += 1
	newDict ={}

	if metID == 1:
		parent = root.keys()[0]
		newDict.update({"id": metID, "name": nodeWrapper(parent, 114, 100, 28), "data": {}, "children": []})
		newDict['data'].update(popupBuilder({"smiles":parent}, metabolite_keys))
		root = root[parent]
	else:
		newDict.update({"id": metID, "name": nodeWrapper(root['smiles'], 114, 100, 28), "data": {}, "children": []})
		# newDict['data'].update({"degradation": root['degradation']})
		newDict['data'].update(popupBuilder(root, metabolite_keys))

	for key, value in root.items():
		if isinstance(value, dict):
			for key2, value2 in root[key].items():
				root2 = root[key][key2]
				if len(root2) > 0: 
					newDict['children'].append(traverse(root2))

	return newDict


def nodeWrapper(smiles, height, width, scale, key=None):
	"""
	Wraps image html tag around
	the molecule's image source

	Inputs: smiles, height, width, scale, key

	Returns: html of wrapped image
	"""

	# 1. Get image from smiles
	post = {
		"smiles": smiles,
		"scale": scale,
		"height": height,
		"width": width
	}
	request = HttpRequest()
	request.POST = post
	results = jchem_rest.smilesToImage(request)

	# 2. Get imageUrl out of results
	data = json.loads(results.content) # json string --> dict
	img, imgScale = '', ''
	if 'data' in data:
		root = data['data'][0]['image']
		if 'image' in root:
			img = changeImageIP(root['image'])

	# 3. Wrap imageUrl with <img>
	html = imgTmpl().render(Context(dict(smiles=smiles, img=img, height=height, width=width, scale=scale, key=key)))	
	return html


def imgTmpl():
	imgTmpl = """
	<img class="metabolite" id="{{key|default:"none"}}" 
		alt="{{smiles}}" src="data:image/gif;base64,{{img}}"
		width="{{width}}" height="{{height}}" /> 
	"""
	return Template(imgTmpl)


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
	html += nodeWrapper(root['smiles'], None, 250, 100)
	html += '</td></tr>'
	for key, value in root.items():
		if key in paramKeys:

			# Convert other types (e.g., float, int) to string
			if not isinstance(value, unicode):
				value = str(value)

			dataProps[key] = value

			html += '<tr><td>' + key + '</td>'
			html += '<td>' + value + '</td></tr>'
	html += '</table>'

	dataProps["html"] = html 

	return dataProps


def changeImageIP(url):
	"""
	Changing IP address from internal CGI to intranet-facing address
	for image urls 

	I.e., http://172.20.100.12/imageUrl --> http://134.67.114.2/imageUrl 
	""" 
	if 'CTS_JCHEM_SERVER_INTRANET' in os.environ:
		return url.replace(os.environ['CTS_JCHEM_SERVER'], os.environ['CTS_JCHEM_SERVER_INTRANET'])
	else:
		return url


