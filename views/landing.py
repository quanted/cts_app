from django.template.loader import render_to_string
from django.http import HttpResponse
import importlib
import linksLeft
import links_left
import os


def ctsLandingPage(request):
    text_file2 = open(os.path.join(os.environ['PROJECT_PATH'], 'cts_app/views/main_text.txt'),'r')
    xx = text_file2.read()

    #drupal template for header with bluestripe
    #html = render_to_string('01epa_drupal_header.html', {})
    html = render_to_string('01epa_drupal_header.html', {
        'SITE_SKIN': os.environ['SITE_SKIN'],
        'title': "CTS"
    })
    #html = render_to_string('01uberheader_main_drupal.html', {
    #    'SITE_SKIN': os.environ['SITE_SKIN'],
    #    'TITLE': u"\u00FCbertool"
    #})
    html += render_to_string('02epa_drupal_header_bluestripe_onesidebar.html', {})
    html += render_to_string('03epa_drupal_section_title_cts.html', {})

    #main body of text
    #html += render_to_string('04uber_drupal_frog_intro.html', {})
    #http://jsfiddle.net/9zGQ8/

    html += render_to_string('06cts_ubertext_start_index_drupal.html', {
        # 'TITLE': 'Chemical Transformation Simulator',
        'TEXT_PARAGRAPH': xx
    })
    html += render_to_string('07ubertext_end_drupal.html', {})
    html += links_left.ordered_list(model='cts')  # fills out 05ubertext_links_left_drupal.html

    #scripts and footer
    html += render_to_string('09epa_drupal_ubertool_css.html', {})
    #html += render_to_string('09epa_drupal_ubertool_scripts.html', {})
    html += render_to_string('09epa_drupal_cts_css.html')
    html += render_to_string('09epa_drupal_cts_scripts.html')
    html += render_to_string('10epa_drupal_footer.html', {})

    response = HttpResponse()
    response.write(html)

    return response


# def ctsLandingPage(request):
#     text_file2 = open(os.path.join(os.environ['PROJECT_PATH'], 'cts_app/views/main_text.txt'),'r')
#     xx = text_file2.read()

#     html = render_to_string('01cts_uberheader.html', {})
#     html = html + render_to_string('02cts_uberintroblock_nomodellinks.html', {})
#     html = html + linksLeft.linksLeft()
#     html = html + render_to_string('04cts_ubertext_start_index.html', {
#             'text_paragraph':xx
#             })
#     html = html + render_to_string('04cts_ubertext_end.html',{})
#     html = html + render_to_string('05cts_ubertext_links_right.html', {})
#     html = html + render_to_string('06cts_uberfooter.html', {'links': ''})

#     response = HttpResponse()
#     response.write(html)

#     return response