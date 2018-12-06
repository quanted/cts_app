from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
import json
import logging
import io
from cts_app.cts_calcs.calculator import Calculator
from cts_app.models.gentrans.gentrans_tables import buildMetaboliteTableForPDF
from django.core.cache import cache
from django.conf import settings



def cts_stress_page(request):
    html = render_to_string('cts_stress_page.html', request=request)
    response = HttpResponse()
    response.write(html)
    return response



@require_POST
def cts_stress_html_download(request):
	"""
	Saves output as HTML
	"""
	input_str = request.POST.get('stress_html')
	packet = io.StringIO(input_str)  # write to memory
	jid = Calculator().gen_jid()  # create timestamp
	response = HttpResponse(packet.getvalue(), content_type='application/html')
	response['Content-Disposition'] = 'attachment; filename=' + 'stress_results_' + jid + '.html'
	packet.close()
	return response