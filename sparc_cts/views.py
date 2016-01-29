# from django.conf import settings # This urls.py file is looking for the TEST_CTS_PROXY_URL variable in the project settings.py file.
from django.shortcuts import render
from django.http import HttpResponse

import logging
import os
import requests
import json
from sparc_calculator import SparcCalc


def request_manager(request):

    try:
        calc = request.POST.get("calc")
        props = request.POST.getlist("props[]")
        structure = request.POST.get("chemical")
        single_prop = request.POST.get('single_prop') # is None if doesn't exist..

        logging.info("Incoming data to SPARC: {}, {}, {} (calc, props, chemical)".format(calc, props, structure))
        logging.info("Single prop: {}".format(single_prop))

        post_data = {
            "calc": calc,
            "props": props
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

        for prop in props:

            logging.info("PROP: {}".format(prop))

            if prop == 'ion_con':
                response = calcObj.makeCallForPka() # response as d ict returned..
                ion_con_response = {
                    'calc': 'sparc',
                    'prop': 'ion_con',
                    'data': calcObj.getPkaResults(response)
                }
                sparc_results.append(ion_con_response)
                # del props[props.index('ion_con')]

            if prop == 'kow_wph':
                ph = request.POST.get('ph') # get PH for logD calculation..
                response = calcObj.makeCallForLogD() # response as dict returned..
                kow_wph_response = {
                    'calc': 'sparc',
                    'prop': 'kow_wph',
                    'data': calcObj.getLogDForPH(response, ph)
                }
                sparc_results.append(kow_wph_response)
                # del props[props.index('kow_wph')]

        logging.info("props: {}".format(props))
        logging.info("length: {}".format(len(props)))

        logging.info("prop map {}".format(calcObj.propMap.keys()))
        prop_map = calcObj.propMap.keys()
        if any(prop in prop_map for prop in props):
            logging.info("### making multi property request ###")
            multi_response = calcObj.makeDataRequest()
            if 'calculationResults' in multi_response:
                multi_response = calcObj.parseMultiPropResponse(multi_response['calculationResults'])
                for prop_obj in multi_response:
                    logging.info("prop: {}".format(prop_obj['prop']))
                    if prop_obj['prop'] in props:
                        sparc_results.append(prop_obj)

        logging.info("SPARC RESULTS: {}".format(sparc_results))

        post_data.update({'data': sparc_results})

        return HttpResponse(json.dumps(post_data), content_type='application/json')


        # if 'calculationResults' in multi_response:
        #     # append ion_con or kow_wph to multi prop response:
        #     multi_response['calculationResults'].append(ion_con_response)
        #     multi_response['calculationResults'].append(kow_wph_response)




        # # TODO: Handle request key for getting pka or ion_con props!!!
        # if single_prop == 'ion_con':
        #     # make request to pka:
        #     response = calcObj.makeCallForPka()
        #     post_data = {
        #         'data': calcObj.getPkaResults(response),
        #         'calc': calc,
        #         'prop': single_prop
        #     }
        #     logging.info("sparc post data: {}".format(post_data))
        #     return HttpResponse(json.dumps(post_data), content_type='application/json')
        # elif single_prop == 'kow_wph':
        #     # make request to logD:
        #     ph = request.POST.get('ph') # get PH for logD calculation..
        #     response = calcObj.makeCallForLogD()
        #     post_data = { 
        #         'data': calcObj.getLogDForPH(response, ph),
        #         'calc': calc,
        #         'prop': single_prop
        #     }
        #     logging.info("sparc post data: {}".format(post_data))
        #     return HttpResponse(json.dumps(post_data), content_type='application/json')
        # else:
        #     # business as usual:
        #     returnedData = calcObj.makeDataRequest() # make call for data!
        #     post_data.update({"calc": "sparc", "props": props, "data": returnedData}) # add that data
        #     logging.info("SPARC POST Data: {}".format(post_data))
        #     return HttpResponse(json.dumps(post_data), content_type='application/json')

    except requests.HTTPError as e:
        logging.warning("HTTP Error occurred: {}".format(e))
        return HttpResponse(e.msg, status=e.code, content_type='text/plain')

    except ValueError as ve:
        logging.warning("POST data is incorrect: {}".format(ve))
        post_data.update({"error": "{}".format(ve)})
        return HttpResponse(json.dumps(post_data), content_type='application/json')

    except requests.exceptions.ConnectionError as ce:
        logging.warning("Connection error occurred: {}".format(ce))
        post_data.update({"error": "connection error"})
        return HttpResponse(json.dumps(post_data), content_type='application/json')