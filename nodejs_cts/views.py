__author__ = 'np'

from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt

import logging
import os
import requests
import json
import redis

from sparc_cts.views import request_manager as sparc_manager
from test_cts.views import request_manager as test_manager
from epi_cts.views import request_manager as epi_manager
from chemaxon_cts.views import request_manager as chemaxon_manager


# r = redis.StrictRedis(host='localhost', port=6379, db=0) # instantiate redis (where should this go???)
# logging.info("django redis client instantiated: {}".format(r))

# @csrf_exempt
def request_manager(request):
    logging.info("inside request manager!")
    # logging.info("redis: {}".format(dir(r)))

    try:

        r = redis.StrictRedis(host='localhost', port=6379, db=0) # instantiate redis (where should this go???)
        logging.warning("connected to redis!")
        logging.warning("incoming message to cts nodejs request manager: {}".format(request.POST))

        node_data = request.POST.get('message')
        # node_data = request.POST.get('data')
        # calcs_props_dict = request.POST.get('data') # incoming message from socket server
        sessionid = request.POST.get('sessionid') # session id created w/ client's socket id on node server
        # chemical = request.POST.get('chem')

        logging.warning("nodejs request manager received message: {}".format(node_data))
        logging.warning("for session id: {}".format(sessionid))


        # this is another place the calls could be looped??????
        # NOTE: i feel like having the calls parsed out here on the 
        # django side is going to fire everything sequentially!
        # i may have to do them either from the front like usual
        # or, if possible, the node server code!
    

        data_obj = json.loads(node_data)

        logging.warning("node data: {}".format(data_obj))
        logging.warning(type(data_obj))

        for calc, props_list in data_obj['data'].items():

            calc_data = {'chemical': data_obj['chem'], 'calc': calc} # initialize data obj for calc
            logging.warning("calc_data: {}".format(calc_data))
            logging.warning("props_list: {}".format(props_list))

            # if calc == 'sparc':
            #     data.update({'props': props_list}) # send whole list of props! (sparc deals with the details)
            #     request = requests.Request(data=calc_data)
            #     calc_data = sparc_manager(request)
            #     logging.warning("{} data for {} props coming into cts-node api".format(calc, props_list))
            #     r.publish(sessionid, calc_data)
            # elif calc == 'test':
            #     # send whole list of props! (sparc deals with the details)
            #     data.update({'props': props_list}) # send whole list of props! (sparc deals with the details)
            #     request = requests.Request(data=calc_data)
            #     calc_data = sparc_manager(request)
            #     logging.warning("{} data for {} props coming into cts-node api".format(calc, props_list))
            #     r.publish(sessionid, calc_data)
            # elif calc == 'epi':
            #     # one at a time, i think
            if calc == 'chemaxon':
                # one at a time, i think
                for prop in props_list:
                    logging.warning("prop: {}".format(prop))
                    calc_data.update({'prop': prop, 'service': 'getPchemProps'})
                    request = HttpRequest()
                    request.POST = calc_data
                    returned_data = chemaxon_manager(request).content
                    logging.warning("{} data: {}".format(calc, returned_data))
                    logging.warning(type(returned_data))
                    r.publish(sessionid, returned_data)
            # else:
                # shouldn't get here!



        # returned_data = json.dumps({'calc': 'chemaxon', 'prop': 'water_sol', 'data': 140.12})
        # r = redis.StrictRedis(host='localhost', port=6379, db=0) # instantiate redis (where should this go???)
        # r.publish(sessionid,  'data: ' + returned_data) # pub message w/ user's session id as channel
        # r.publish(sessionid, returned_data)

        return HttpResponse("~~~~ it worked!")

    except Exception as e:
        logging.warning(e)
        # raise
        return HttpResponse("error occured in nodejs request manager")