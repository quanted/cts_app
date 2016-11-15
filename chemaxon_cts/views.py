from django.http import HttpResponse, HttpRequest
import requests
import jchem_rest
import logging
import json
import redis
from jchem_calculator import JchemProperty
from REST.smilesfilter import filterSMILES
# from requests_futures.sessions import FuturesSession
from models.gentrans import data_walks


# TODO: get these from the to-be-modified jchem_rest class..
services = ['getChemDetails', 'getChemSpecData', 'smilesToImage', 'convertToSMILES',
            'getTransProducts', 'getPchemProps', 'getPchemPropDict', 'getJchemVersion',
            'getMolecularInfo']

methods = ['KLOP', 'VG', 'PHYS']

redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0)


def request_manager(request):
    """
    Redirects request from frontend to the
    approriate jchem web service. All calls going
    from browser to cts for jchem go through
    here first.
    Expects: data for requested service, and
    which name of service to call
    Format: {"service": "", "data": {usual POST data}}
    """

    service = request.POST.get('service')
    chemical = request.POST.get('chemical')
    prop = request.POST.get('prop')
    sessionid = request.POST.get('sessionid')  # None if it doesn't exist
    method = request.POST.get('method')
    ph = request.POST.get('ph')
    node = request.POST.get('node') # TODO: keep track of nodes without bringing node obj along for the ride!
    calc = request.POST.get('calc')
    run_type = request.POST.get('run_type')
    workflow = request.POST.get('workflow')

    try:
        props = request.POST.get("props[]")
        if not props:
            props = request.POST.getlist("props")
    except AttributeError:
        props = request.POST.get("props")

    # session = FuturesSession()  # currently not used..
    session = None

    if service == 'getTransProducts':
        # getTransProducts chemaxon service..

        request = HttpRequest()
        # from gentrans model:
        request.POST = {
            'structure': chemical,
            'generationLimit': 1,  # make sure to get this from front end
            'populationLimit': 0,
            'likelyLimit': 0.001,
            'transformationLibraries': ['human_biotransformation'],  # get from front end as well!!!
            'excludeCondition': ""  # 'generateImages': False
        }

        response = jchem_rest.getTransProducts(request)
        data_walks.j = 0
        data_walks.metID = 0
        results = data_walks.recursive(response.content, 1)

        data_obj = {
            'calc': "chemaxon",
            'prop': "products",
            'node': node,
            'data': json.loads(results),
            'chemical': chemical,
            'workflow': 'gentrans',
            'run_type': 'batch'
        }

        if redis_conn and sessionid:
            result_json = json.dumps(data_obj)
            redis_conn.publish(sessionid, result_json)
        else:
            return HttpResponse(json.dumps(data_obj), content_type='application/json')

    elif service == 'getSpeciationData':
        from models.chemspec import chemspec_output

        spec_inputs = request.POST.get('speciation_inputs')

        model_params = {
            'run_type': 'single',
            'chem_struct': None,
            'smiles': chemical,
            'orig_smiles': None,
            'iupac': None,
            'formula': None,
            'mass': None,
            'get_pka': True,
            'get_taut': None,
            'get_stereo': None,
            'pKa_decimals': None,
            'pKa_pH_lower': None,
            'pKa_pH_upper': None,
            'pKa_pH_increment': None,
            'pH_microspecies': None,
            'isoelectricPoint_pH_increment': None,
            'tautomer_maxNoOfStructures': None,
            'tautomer_pH': None,
            'stereoisomers_maxNoOfStructures': None
        }

        for key, value in model_params.items():
            if key in spec_inputs:
                # will it matter than spec_inputs key:val are unicode????
                model_params.update({key: spec_inputs[key]})

        # here's where calling chemspec model would be gud...

        request = HttpRequest()
        request.POST = model_params
        request.method = "POST"  # required because of chemspec_output @request_POST???

        chemspec_obj = chemspec_output.chemspecOutputPage(request)

        data_obj = {
            'calc': "chemaxon",
            'prop': "speciation_results",
            'node': node,
            'data': chemspec_obj.jchemDictResults,
            'chemical': chemical,
            'workflow': 'chemaxon',
            'run_type': 'batch'
        }

        if redis_conn and sessionid:
            result_json = json.dumps(data_obj)
            redis_conn.publish(sessionid, result_json)

    else:

        if run_type == 'rest':
            props = [prop]
            return getPchemPropData(chemical, sessionid, method, ph, node, calc, run_type, props, session)
        else:
            # no return w/ web sockets?
            getPchemPropData(chemical, sessionid, method, ph, node, calc, run_type, props, session)


def getPchemPropData(chemical, sessionid, method, ph, node, calc, run_type, props, session):

    postData = {
        'calc': calc,
        # 'props': props
    }

    logging.warning("post data: {}".format(postData))

    if props:
        chemaxon_results = []
        for prop in props:

            logging.info("requesting chemaxon {} data".format(prop))

            data_obj = {'calc': calc, 'prop':prop, 'node': node, 'chemical': chemical}

            if run_type:
                data_obj.update({'run_type': run_type})

            try:
                if prop == 'kow_wph' or prop == 'kow_no_ph':
                    for method in methods:

                        new_data_obj = {}
                        new_data_obj.update({
                            'calc': calc,
                            'prop': prop,
                            'chemical': chemical,
                            'node': node
                        })

                        results = sendRequestToWebService("getPchemProps", chemical, prop, ph, method, sessionid, node, session)  # returns json string
                        new_data_obj.update({'data': results['data'], 'method': method})

                        logging.info("chemaxon results: {}".format(results))

                        if redis_conn and sessionid:
                            result_json = json.dumps(new_data_obj)
                            redis_conn.publish(sessionid, result_json)
                        else:
                            chemaxon_results.append(new_data_obj)

                else:
                    results = sendRequestToWebService("getPchemProps", chemical, prop, ph, None, sessionid, node, session)  # returns json string
                    data_obj.update({'data': results['data']})

                    logging.info("chemaxon results: {}".format(results))

                    if redis_conn and sessionid:
                        result_json = json.dumps(data_obj)
                        redis_conn.publish(sessionid, result_json)
                    else:
                        chemaxon_results.append(data_obj)

            except Exception as err:
                logging.warning("Exception occurred getting chemaxon data: {}".format(err))
                logging.info("session id: {}".format(sessionid))

                data_obj.update({'error': "cannot reach chemaxon calculator"})

                if redis_conn and sessionid:
                    redis_conn.publish(sessionid, json.dumps(data_obj))
                else:
                    chemaxon_results.append(data_obj)

        redis_conn.delete(sessionid)  # clear user's job cache from redis

        # pack up all results to send at once if using http:
        postData.update({'data': chemaxon_results})

        # if not redis_conn and not sessionid:
        if not sessionid:
            # send response over http (for accessing as REST service)
            return HttpResponse(json.dumps(postData), content_type='application/json')

    return


def sendRequestToWebService(service, chemical, prop, phForLogD=None, method=None, sessionid=None, node=None, session=None):
    """
    Makes call to jchem rest service
    """
    request = requests.Request(data={'chemical': chemical})
    response = None
    if service == 'getChemDetails':
        try:
            response = jchem_rest.convertToSMILES(request)  # convert chemical to smiles
            response = json.loads(response.content)  # get json data
            filtered_smiles = filterSMILES(response['structure'])  # call CTS REST SMILES filter
            request.data = {'chemical': filtered_smiles}
            response = jchem_rest.getChemDetails(request)  # get chemical details
            response = json.loads(response.content)
        except Exception as e:
            raise e # TODO: build HTTP-code-specific error handling at portal.py
        response = jchem_rest.getChemDetails(request).content
    elif service == 'getChemSpecData':
        response = jchem_rest.getChemSpecData(request).content
    elif service == 'smilesToImage':
        response = jchem_rest.smilesToImage(request).content
    elif service == 'convertToSMILES':
        response = jchem_rest.convertToSMILES(request).content
    elif service == 'getPchemProps':
        response = getJchemPropData(chemical, prop, phForLogD, method, sessionid, node, session)
    return response


def getJchemPropData(chemical, prop, phForLogD=None, method=None, sessionid=None, node=None, session=None):
    """
    Calls jchem web services from chemaxon and
    wraps data in a CTS data object (keys: calc, prop, method, data)
    """

    resultDict = {"calc": "chemaxon", "prop": prop}

    result = ""
    if prop == 'water_sol':
        propObj = JchemProperty.getPropObject('solubility')
        propObj.makeDataRequest(chemical, None, session)
        result = propObj.getSolubility()
    elif prop == 'ion_con':
        propObj = JchemProperty.getPropObject('pKa')
        propObj.makeDataRequest(chemical, None, session)

        pkas = propObj.getMostAcidicPka() + propObj.getMostBasicPka()
        pkas.sort()

        result = {'pKa': pkas}
        # result = {'pKa': propObj.getMostAcidicPka(), 'pKb': propObj.getMostBasicPka()}
    elif prop == 'kow_no_ph':
        propObj = JchemProperty.getPropObject('logP')
        propObj.makeDataRequest(chemical, method, session)
        result = propObj.getLogP()
    elif prop == 'kow_wph':
        propObj = JchemProperty.getPropObject('logD')
        propObj.makeDataRequest(chemical, method, session)
        result = propObj.getLogD(phForLogD)
    else:
        result = None

    # ADD METHOD KEY:VALUE IF LOGD OR LOGP...
    resultDict['data'] = result
    if method:
        resultDict['method'] = method

    return resultDict
