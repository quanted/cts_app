from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect


def cts_stress_page(request):

    html = render_to_string('cts_stress_page.html')

    response = HttpResponse()
    response.write(html)
    return response