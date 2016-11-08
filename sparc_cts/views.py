# from django.conf import settings # This urls.py file is looking for the TEST_CTS_PROXY_URL variable in the project settings.py file.
from django.shortcuts import render
from django.http import HttpResponse
from django.core.cache import cache

import logging
import requests
import json
import redis

from sparc_calculator import SparcCalc

redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0)  # instantiate redis (where should this go???)


def request_manager(request):

    calc = request.POST.get("calc")
    try:
        props = request.POST.get("props[]")
        if not props:
            props = request.POST.getlist("props")
    except AttributeError:
        props = request.POST.get("props")

    structure = request.POST.get("chemical")
    sessionid = request.POST.get('sessionid')
    node = request.POST.get('node')
    prop = request.POST.get('prop')
    run_type = request.POST.get('run_type')

    # logging.info("Incoming data to SPARC: {}, {}, {} (calc, props, chemical)".format(calc, props, structure))

    post_data = {
        "calc": "sparc",
        "props": props,
        'node': node
    }

    ############### Filtered SMILES stuff!!! ################################################
    # filtered_smiles = parseSmilesByCalculator(structure, "sparc") # call smilesfilter

    # logging.info("SPARC Filtered SMILES: {}".format(filtered_smiles)) 

    # if '[' in filtered_smiles or ']' in filtered_smiles:
    #   logging.warning("SPARC ignoring request due to brackets in SMILES..")
    #   post_data.update({'error': "SPARC cannot process charged species or metals (e.g., [S+], [c+])"})
    #   return HttpResponse(json.dumps(post_data), content_type='application/json')
    ###########################################################################################

    calcObj = SparcCalc(structure)

    ion_con_response, kow_wph_response, multi_response = None, None, None
    sparc_results = []

    # synchronous calls for ion_con, kow_wph, and the rest:

    # don't need this loop, just do "if 'ion_con' in prop: make request"

    logging.warning("sparc props: {}".format(props))

    sparc_response = {
        'calc': 'sparc',
        # 'prop': prop,
        'node': node,
        'chemical': structure,
        'request_post': request.POST
    }

    if run_type == 'rest':
        props = [prop]


    try:
        # if prop == 'ion_con':
        if 'ion_con' in props:
            response = calcObj.makeCallForPka() # response as d ict returned..
            pka_data = calcObj.getPkaResults(response)
            sparc_response.update({'data': pka_data, 'prop': 'ion_con'})
            logging.info("response: {}".format(sparc_response))
            # sparc_results.append(ion_con_response)
            result_json = json.dumps(sparc_response)
            if redis_conn and sessionid:
                redis_conn.publish(sessionid, result_json)
            else:
                return HttpResponse(result_json, content_type='application/json')

        # if prop == 'kow_wph':
        if 'kow_wph' in props:
            ph = request.POST.get('ph') # get PH for logD calculation..
            response = calcObj.makeCallForLogD() # response as dict returned..
            sparc_response.update({'data': calcObj.getLogDForPH(response, ph), 'prop': 'kow_wph'})
            logging.info("response: {}".format(sparc_response))
            # sparc_results.append(kow_wph_response)
            result_json = json.dumps(sparc_response)
            if redis_conn and sessionid:
                redis_conn.publish(sessionid, result_json)
            else:
                return HttpResponse(result_json, content_type='application/json')

        prop_map = calcObj.propMap.keys()
        # if any(prop not in ['ion_con', 'kow_wph'] for prop in props):
        # for prop in props:

        logging.warning("actually making multi prop call")

        multi_response = calcObj.makeDataRequest()
        if 'calculationResults' in multi_response:

            logging.warning("about to parse responses")

            logging.warning("props: {}".format(props))
            # logging.warning("prop: {}".format(prop))

            multi_response = calcObj.parseMultiPropResponse(multi_response['calculationResults'])
            for prop_obj in multi_response:
                # if prop_obj['prop'] in props:
                # if prop_obj['prop'] == prop:
                if prop_obj['prop'] in props and prop_obj != 'ion_con' and prop_obj != 'kow_wph':
                    prop_obj.update({'node': node, 'chemical': structure})
                    logging.info("response: {}".format(prop_obj))
                    result_json = json.dumps(prop_obj) 
                    if redis_conn and sessionid:
                        redis_conn.publish(sessionid, result_json)
                    else:
                        return HttpResponse(result_json, content_type='application/json')
                    # could send each calc-prop-data instead of list of them..

    except Exception as err:
        logging.warning("Exception occurred getting SPARC data: {}".format(err))
        logging.info("session id: {}".format(sessionid))

        for prop in props:

            post_data.update({
                'error': "data request timed out",
                'prop': prop,
                'request_post': request.POST
            })

            if redis_conn and sessionid: 
                redis_conn.publish(sessionid, json.dumps(post_data))
            else:
                return HttpResponse(json.dumps(post_data), content_type='application/json')