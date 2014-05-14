"""
Created on Tue Jan 03 13:30:41 2012

@author: mg
"""
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
from analysis import analysis_parameters

class ctsInputPage(webapp.RequestHandler):
    def get(self):
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01cts_uberheader.html', {'title'})
        html = html + template.render (templatepath + 'cts-jquery.html', {})
        html = html + template.render(templatepath + '02cts_uberintroblock_wmodellinks.html', {'model':'analysis','page':'input'})
        html = html + template.render (templatepath + '03cts_ubertext_links_left.html', {})
        html = html + template.render(templatepath + '04ubercts_start.html', {
                'model':'analysis', 
                'model_attributes':'Chemical Structural Analysis'})
        html = html + template.render (templatepath + '04uberinput_tabbed_nav.html', {
                'nav_dict': {
                    'class_name': ['Chemical', 'Speciation'],
                    'tab_label': ['Chemical Editor', 'Chemical Speciation']
                    }
                })
        html = html + template.render(templatepath + 'cts.html', {})
        html = html + str(analysis_parameters.form())
#        html = html + template.render(templatepath + 'jschemeditor.html', {})
        html = html + template.render(templatepath + '04ubercts_end.html', {'sub_title': 'Submit'})
        html = html + template.render(templatepath + '06cts_uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', ctsInputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
