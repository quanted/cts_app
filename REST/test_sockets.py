"""
Views for HTML and JS for establishing a web socket
connection with the nodejs server

nginx: port 80
django: port 8081
nodejs: port 4000
"""
from django.template.loader import render_to_string
from django.http import HttpResponse
import logging
import json


html = render_to_string('cts_socket_test.html')

return HttpResponse(html)