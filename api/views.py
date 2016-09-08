from django.shortcuts import render

# Create your views here.
def showSwaggerPage(request):
	"""
	display swagger.json with swagger UI
	for CTS API docs/endpoints
	"""
	swag = open('static/docs/swagger.json', 'r').read()

	
	
	return HttpResponse(swag, mimetype='application/json')