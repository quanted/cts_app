import logging
import json
from django.http import HttpRequest
from chemaxon_cts import jchem_rest
from django.template import Context, Template, defaultfilters

"""
10-31-14 (np)
Recursively walks n-nested dictionary
in json format and restructures the data to
comply with the jquery flow chart library
used: jit (thejit.org)
"""


def recursive(jsonStr):
    """
	Starting point for walking through
	metabolites dictionary and building json
	that thejit (visualization javascript
	library) understands
	"""
    jsonDict = json.loads(jsonStr)
    root = jsonDict['results']
    reDict = {}
    parent = root.keys()[0]
    reDict.update(traverse(root))
    return json.dumps(reDict)


metID = 0  # unique id for each node
metabolite_keys = ['smiles', 'accumulation', 'production', 'transmissivity', 'generation']

def traverse(root):
    """
	For gentrans model output - metabolites tree
	"""

    global metID
    metID += 1
    newDict = {}

    logging.info("metabolites: {}".format(metID))

    tblID = "{}_table".format(metID)  # id for node's tooltip table

    if metID == 1:
        parent = root.keys()[0]
        newDict.update({"id": metID, "name": nodeWrapper(parent, 114, 100, 28), "data": {}, "children": []})
        newDict['data'].update(popupBuilder({"smiles": parent, "generation": "0"}, metabolite_keys, "{}".format(metID),
                                            "Metabolite Information"))
        root = root[parent]
    else:
        if root['generation'] > 0:
            newDict.update({"id": metID, "name": nodeWrapper(root['smiles'], 114, 100, 28), "data": {}, "children": []})
            newDict['data'].update(popupBuilder(root, metabolite_keys, "{}".format(metID), "Metabolite Information"))

    for key, value in root.items():
        if isinstance(value, dict):
            for key2, value2 in root[key].items():
                root2 = root[key][key2]
                if len(root2) > 0 and 'children' in newDict:
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
    data = json.loads(results.content)  # json string --> dict
    img, imgScale = '', ''
    if 'data' in data:
        root = data['data'][0]['image']
        if 'image' in root:
            img = root['image']

    # 3. Wrap imageUrl with <img>
    html = imgTmpl().render(Context(dict(smiles=smiles, img=img, height=height, width=width, scale=scale, key=key)))
    return html


def imgTmpl():
    imgTmpl = """
	<img class="metabolite" id="{{key|default:""}}"
		alt="{{smiles}}" src="data:image/png;base64,{{img}}"
		width="{{width}}" height="{{height}}" /> 
	"""
    return Template(imgTmpl)


def popupBuilder(root, paramKeys, molKey=None, header=None):
    """
	Wraps molecule data (e.g., formula, iupac, mass, 
	smiles, image) in table

	Inputs:
	root - dictionary of items to wrap in table
	paramKeys - keys to use for building table
	molKey - (optional) add id to wrap table
	header - (optional) add header above key/values 

	Returns: dictionary where html key is 
	the wrapped html and the other keys are
	same as the input keys
	"""

    # propKeys = ['smiles', 'accumulation', 'production', 'transmissivity', 'generation']
    dataProps = {key: None for key in paramKeys}  # metabolite properties

    html = '<div id="{}_div" class="nodeWrapDiv"><div class="metabolite_img" style="float:left;">'.format(molKey)
    # html += nodeWrapper(root['smiles'], None, 250, 100)
    html += nodeWrapper(root['smiles'], None, 250, 70)
    html += '</div>'

    if molKey:
        html += '<table class="ctsTableStylin" id="{}_table">'.format(molKey)
    else:
        html += '<table class="ctsTableStylin">'

    if header:
        html += '<tr class="header"><th colspan="2">' + header + '</th></tr>'

    for key, value in root.items():
        if key in paramKeys:

            # Convert other types (e.g., float, int) to string
            if not isinstance(value, unicode) and not (isinstance(value, str)):
                value = str(round(float(value), 3))
            # value = str(value)

            dataProps[key] = value

            html += '<tr><td>' + key + '</td>'
            html += '<td>' + value + '</td></tr>'
    html += '</table></div>'

    dataProps["html"] = html

    return dataProps


htmlList = []
def buildTableValues(nodeList, keys, nRound):
    """
    Builds list of dictionary items with
    nodes' key:values for pdf
    """
    for node in nodeList:
        htmlListItem = {}
        for key in keys:
            if key in node:
                htmlListItem.update({key: roundValue(node[key], nRound)})
            elif 'data' in node and key in node['data']:
                htmlListItem.update({key: roundValue(node['data'][key], nRound)})
            elif 'data' in node and 'pchemprops' in node['data']:
                for prop in node['data']['pchemprops']:
                    if key in prop['prop']:
                        htmlListItem.update({key: roundValue(prop['data'], nRound)})
            else:
                htmlListItem.update({key: ''})
        htmlList.append(htmlListItem)
    logging.info("TABLE VALUES FOR PDF: {}".format(htmlList))
    return htmlList


def roundValue(val, n):
    try:
        val = float(val)
        return round(val, n)
    except ValueError:
        return val  # not num, don't round
    except TypeError:
        # accounting for if val is not string or number:
        if isinstance(val, dict):
            # assuming pKa dict
            roundedDict = {}
            for key, values in val.items():
                if isinstance(values, list):
                    pkaList = []
                    for pka in values:
                        pkaList.append(round(pka, n))
                    roundedDict[key] = pkaList
            return roundedDict


# htmlList = []
# def buildTableValues(nodeList, props, nRound):
#     """
#     Builds list of dictionary items with
#     nodes' key:values for pdf
#     """
#     for node in nodeList:
#         htmlListItem = {}
#         for key in props:
#             if key in node:
#                 htmlListItem.update({
#                     key: roundValue(node[key], nRound)
#                 })
#
#             elif 'data' in node and key in node['data']:
#                 htmlListItem.update({
#                     key: roundValue(node['data'][key], nRound)
#                 })
#
#             elif 'data' in node and 'pchemprops' in node['data']:
#                 for prop in node['data']['pchemprops']:
#                     calculator = prop['calc']
#                     if key in prop['prop']:
#                         if calculator in htmlListItem:
#                             htmlListItem[calculator].update({
#                                 key: roundValue(prop['data'], nRound)
#                             })
#                         else:
#                             htmlListItem.update({
#                                 calculator: {key: roundValue(prop['data'], nRound)}
#                             })
#
#             else:
#                 htmlListItem.update({key: ''})
#         htmlList.append(htmlListItem)
#     return htmlList
