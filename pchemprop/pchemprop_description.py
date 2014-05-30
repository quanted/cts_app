# -*- coding: utf-8 -*-
"""
Created on Tue Jan 03 13:30:41 2012

@author: jharston
"""
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import os

class pchempropDescriptionPage(webapp.RequestHandler):
    def get(self):
        text_file = open('pchemprop/pchemprop_description.txt','r')
        x = text_file.read()
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01cts_uberheader.html', {'title'})
        html = html + template.render(templatepath + '02cts_uberintroblock_wmodellinks.html', {'model':'pchemprop','page':'description'})
        html = html + template.render(templatepath + '03cts_ubertext_links_left.html', {})                       
        html = html + template.render(templatepath + '04ubertext_start.html', {
                'model_page':'#', 
                'model_attributes':'Chemical Transformation Simulator Overview', 
                'text_paragraph':x})
        html = html + template.render(templatepath + '04ubertext_nav.html', {'model':'pchemprop'})
        html = html + template.render(templatepath + '04ubertext_end.html', {})
        html = html + template.render(templatepath + '05cts_ubertext_links_right.html', {})
        html = html + template.render(templatepath + '06cts_uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', pchempropDescriptionPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
 