import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import cgi
import cgitb
cgitb.enable()
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import django
from django import forms
from pchemprop import pchemprop_parameters

class pchempropInputPage(webapp.RequestHandler):
    def get(self):
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01cts_uberheader.html', {'title'})
        html = html + template.render(templatepath + '02cts_uberintroblock_wmodellinks.html', {'model':'pchemprop','page':'input'})
        html = html + template.render (templatepath + '03cts_ubertext_links_left.html', {})
        html = html + template.render(templatepath + '04uberinput_start.html', {
                'model':'pchemprop', 
                'model_attributes':'pchemprop Inputs'})
        html = html + str(pchemprop_parameters.pchempropInp())
        html = html + template.render(templatepath + '04uberinput_end.html', {'sub_title': 'Submit'})
        html = html + template.render(templatepath + '05ubertext_tooltips_right.html', {})
        html = html + template.render(templatepath + '06cts_uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', pchempropInputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()