from django.conf import settings # This urls.py file is looking for the TEST_CTS_PROXY_URL variable in the project settings.py file.
from django.shortcuts import render
from django.http import HttpResponse
import urllib2
import logging

# simple_proxy is a method that reaches out to a predefined (in the settings.py file for the project) API server, in this case, hosting TEST endpoints
# It would expect a URL that would hit django that looks like http://yourdjangoserver/test_cts/api/TEST/SMILE/<endpoint>
# As of 10/22/14, TEST is responding to endpoints that include ALL, ALOGP, BP, KLOGP, MLOGP, MP, TEMPLATE, VP, WS, XLOGP, BP/MEASURED, MP/MEASURED, VP/MEASURED, and WS/MEASURED
# TODO: this function is strongly generic, it may be worth considering to use this as a component of the larger ubertool project for CTS/upstream. 
def simple_proxy(request, path):
  TEST_URL = settings.TEST_CTS_PROXY_URL + path
  # TEST_URL = "http://127.0.0.1:8000/test_cts/api/" + path
  logging.warning(request)

  try:
    async_request = urllib2.urlopen(TEST_URL)
    async_data = async_request.read()
  except urllib2.HTTPError as e:
    return HttpResponse(TEST_URL+e.msg, status=e.code, content_type='text/plain')
  else: 
    return HttpResponse(async_data, status=async_request.code, content_type=async_request.headers.typeheader) 
      
def index(request,model):
  return render(request, 'test_cts/index')

def calc_kow(request):
  return render(request, 'calc_kow.html')
