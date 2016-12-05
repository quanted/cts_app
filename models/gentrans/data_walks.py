import logging
import json
from django.http import HttpRequest
# from chemaxon_cts import jchem_rest
from cts_calcs.chemaxon_cts import jchem_rest
from django.template import Context, Template, defaultfilters

"""
10-31-14 (np)
Recursively walks n-nested dictionary
in json format and restructures the data to
comply with the jquery flow chart library
used: jit (thejit.org)
"""


def recursive(jsonDict, gen_limit):
    """
	Starting point for walking through
	metabolites dictionary and building json
	that thejit (visualization javascript
	library) understands
	"""
    root = jsonDict['results']
    reDict = {}
    parent = root.keys()[0]
    reDict.update(traverse(root, gen_limit))
    return json.dumps(reDict)


metID = 0  # unique id for each node
metabolite_keys = ['smiles', 'formula', 'iupac', 'mass', 'accumulation', 'production', 'transmissivity', 'generation', 'routes', 'exactMass']
image_scale = 50

def traverse(root, gen_limit):
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
        newDict.update({"id": metID, "name": nodeWrapper(parent, 114, 100, image_scale, metID, 'svg', True), "data": {}, "children": []})
        # newDict.update({"id": metID, "name": nodeWrapper(parent, None, 100, 28), "data": {}, "children": []})
        newDict['data'].update(popupBuilder({"smiles": parent, "generation": "0"}, metabolite_keys, "{}".format(metID),
                                            "Metabolite Information"))

        request_obj = {'chemical': parent}
        mol_info = jchem_rest.getChemDetails(request_obj)
        
        if 'data' in mol_info:
            for key, val in mol_info['data'][0].items():
                if key in metabolite_keys:
                    newDict['data'].update({key: val})

        # skipping 2nd parent metabolite:
        second_parent = root[parent]['metabolites'].keys()[0]
        root = root[parent]['metabolites'][second_parent]

        # not-skipping version without 2nd parent problem:
        # root = root[parent]
        
    else:
        if root['generation'] > 0 and root['generation'] <= gen_limit:
            newDict.update({"id": metID, "name": nodeWrapper(root['smiles'], 114, 100, image_scale, metID, 'svg', True), "data": {}, "children": []})
            # newDict.update({"id": metID, "name": nodeWrapper(root['smiles'], None, 100, 28), "data": {}, "children": []})
            newDict['data'].update(popupBuilder(root, metabolite_keys, "{}".format(metID), "Metabolite Information"))

            request_obj = {'chemical': root['smiles']}
            mol_info = jchem_rest.getChemDetails(request_obj)
            
            if 'data' in mol_info:
                for key, val in mol_info['data'][0].items():
                    if key in metabolite_keys:
                        newDict['data'].update({key: val})

    for key, value in root.items():
        if isinstance(value, dict):
            for key2, value2 in root[key].items():
                root2 = root[key][key2]
                if len(root2) > 0 and 'children' in newDict and root['generation'] < gen_limit:
                # if len(root2) > 0 and 'children' in newDict and root2['generation'] < gen_limit:
                    newDict['children'].append(traverse(root2, gen_limit))

    return newDict


def nodeWrapper(smiles, height, width, scale, key=None, img_type=None, isProduct=None):
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
        "width": width,
        # "type": img_type
    }

    if img_type:
        post.update({'type': img_type})

    results = jchem_rest.smilesToImage(post)

    # 2. Get imageUrl out of results
    img, imgScale = '', ''
    if 'data' in results:
        root = results['data'][0]['image']
        if 'image' in root:
            img = root['image']

    # 3. Wrap imageUrl with <img>
    # <img> wrapper for image byte string:
    if img_type and img_type == 'svg':


        # wrap svg in div with background-color set to white on div????
        # html = svgTmpl().render(Context(dict(key=key, svg=img)))
        # html = img  # works but image background is grey...
        if key:
            html = '<div style="background-color:white;"' + 'id="' + str(key) + '">' + img + '</div>'            
        else:
            html = '<div style="background-color:white;">' + img + '</div>'
        
    else:
        html = imgTmpl(isProduct).render(Context(dict(smiles=smiles, img=img, height=height, width=width, scale=scale, key=key)))

    # wrapper for SVG type images:
    # html = data['data'][0]['image']['image']  # expecting svg type now (could affect popups)

    # do the <svg> elements need class and id like imgTmpl below???

    return html


def imgTmpl(isProduct):
    if isProduct:
        imgTmpl = """
        <img class="metabolite" id="{{key|default:""}}"
            alt="{{smiles}}" src="data:image/png;base64,{{img}}"
            width={{width}} height={{height}} /> 
        """        
    else:
        imgTmpl = """
    	<img class="metabolite" id="{{key|default:""}}"
    		alt="{{smiles}}" src="data:image/png;base64,{{img}}"
    		width={{width}} height={{height}} hidden /> 
    	"""
    return Template(imgTmpl)

def svgTmpl():
    # svgTmpl = """
    # <div id="{{key|default:""}}" class="metabolite">
    #     {{svg}}
    # </div>
    # """
    svgTmpl = """
    <div class="metabolite">
        {{svg}}
    </div>
    """
    return Template(svgTmpl)

# def imgTmpl():
#     imgTmpl = """
#     <img class="metabolite" id="{{key|default:""}}"
#         alt="{{smiles}}" src="data:image/png;base64,{{img}}" />
#     """
#     return Template(imgTmpl)


def popupBuilder(root, paramKeys, molKey=None, header=None, isProduct=False):
    """
	Wraps molecule data (e.g., formula, iupac, mass, 
	smiles, image) for hover-over popups in chemspec
    and gentrans outputs.

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
    # html += nodeWrapper(root['smiles'], None, 250, 150)

    # smiles, height, width, scale, key=None, img_type=None

    if isProduct:
        html += nodeWrapper(root['smiles'], None, 250, image_scale, molKey, 'png')  # hidden png for pdf    
    else:
        # html += nodeWrapper(root['smiles'], None, 250, image_scale)  # Molecular Info image, metabolites output
        html += nodeWrapper(root['smiles'], None, 250, image_scale, molKey, 'svg')  # svg popups for chemspec and gentrans outputs
        html += nodeWrapper(root['smiles'], None, 250, image_scale, molKey, None)  # hidden png for pdf

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
                
                if key == 'exactMass':
                    value = str(value)
                else:
                    value = str(round(float(value), 3))
            # value = str(value)

            dataProps[key] = value

            html += '<tr><td>' + key + '</td>'
            html += '<td>' + value + '</td></tr>'
    html += '</table></div>'

    dataProps["html"] = html

    return dataProps


htmlList = []
def buildTableValues(nodeList, checkedCalcsAndProps, mol_info, nRound):
    """
    Builds list of dictionary items with
    nodes' key:values for pdf
    """
    for node in nodeList:
        htmlListItem = {}
        for key in mol_info:
            # molecular information conditional
            if key in node:
                htmlListItem.update({key: roundValue(node[key], nRound)})
            # elif 'data' in node and key in node['data']:
            #     htmlListItem.update({key: roundValue(node['data'][key], nRound)})
            # elif 'data' in node and 'pchemprops' in node['data']:
            #     for prop in node['data']['pchemprops']:
            #         if key in prop['prop']:
            #             htmlListItem.update({key: roundValue(prop['data'], nRound)})
            else:
                htmlListItem.update({key: ''})


    for calc, props in checkedCalcsAndProps.items():
        for prop in props:
            for node in nodeList:
                for chem_data in node['pchemprops']:
                    if prop == 'ion_con':
                        j = 1
                        for pka in chem_data['data']['pKa']:
                            header = "pka_{} ({})".format(j, calc)
                            htmlListItem.update({header: pka})
                            j += 1
                    else:
                        
                        if 'method' in chem_data:
                            header = "{} ({}, {})".format(prop, calc, chem_data['method'])
                        else:
                            header = "{} ({})".format(prop, calc)

                        htmlListItem.update({header: chem_data['data']})

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


# def collapseNest(nestedJson):
    # """
    # walks through n-nested results from
    # recursive function and returns a list
    # of products with a genKey for keeping
    # track of position in tree (e.g., 1.3.1)
    # """
    
    