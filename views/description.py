from django.template.loader import render_to_string
from django.http import HttpResponse
import importlib
import linksLeft
import links_left
import os

def descriptionPage(request, model='none', header='none'):

    viewmodule = importlib.import_module('.views', 'cts_app.models.'+model)
    header = viewmodule.header
    text_file2 = open(os.path.join(os.environ['PROJECT_PATH'], 'cts_app/models/'+model+'/'+model+'_text.txt'),'r')
    xx = text_file2.read()

    #drupal template for header with bluestripe
    #html = render_to_string('01epa_drupal_header.html', {})
    html = render_to_string('01epa_drupal_header.html', {
        'SITE_SKIN': os.environ['SITE_SKIN'],
        'TITLE': "CTS"
    })
    html += render_to_string('02epa_drupal_header_bluestripe_onesidebar.html', {})
    html += render_to_string('03epa_drupal_section_title_cts.html', {})

    html += render_to_string('06cts_ubertext_start_index_drupal.html', {
        'TITLE': header + ' Overview',
        'TEXT_PARAGRAPH': xx
    })
    html += render_to_string('07ubertext_end_drupal.html', {})
    html += links_left.ordered_list('cts/'+model)  # fills out 05ubertext_links_left_drupal.html

    #scripts and footer
    html += render_to_string('09epa_drupal_ubertool_css.html', {})
    html += render_to_string('09epa_drupal_cts_css.html')
    html += render_to_string('09epa_drupal_cts_scripts.html')
    #html += render_to_string('09epa_drupal_ubertool_scripts.html', {})
    html += render_to_string('10epa_drupal_footer.html', {})

    # html = render_to_string('01cts_uberheader.html', {'title': header+' Description'})
    # html = html + render_to_string('02cts_uberintroblock_wmodellinks.html', {'model':model,'page':'description'})
    # html = html + linksLeft.linksLeft()
    # html = html + render_to_string('04cts_ubertext_start.html', {
    #         'model_attributes': header+' Overview',
    #         'text_paragraph':xx})

    # html = html + render_to_string('04cts_ubertext_nav.html', {'model':model})

    # html = html + render_to_string('04cts_ubertext_end.html', {})
    # html = html + render_to_string('05cts_ubertext_links_right.html', {})
    # html = html + render_to_string('06cts_uberfooter.html', {'links': ''})
    
    response = HttpResponse()
    response.write(html)
    return response


def about_page(request, model='none', header='non'):
    
    if model == 'modules':
        text_file2 = open(os.path.join(os.environ['PROJECT_PATH'], 'static_qed/cts/docs/cts_modules_descriptions.txt'),'r')
        header = "CTS Modules"

    elif model == 'pchemcalcs':
        text_file2 = open(os.path.join(os.environ['PROJECT_PATH'], 'static_qed/cts/docs/cts_pchemcalcs_descriptions.txt'),'r')
        header = "P-Chem Calculators"

    elif model == 'reactionlibs':
        text_file2 = open(os.path.join(os.environ['PROJECT_PATH'], 'static_qed/cts/docs/cts_reactionlibs_descriptions.txt'),'r')
        header = "Reaction Libraries"

    xx = text_file2.read()

    #drupal template for header with bluestripe
    #html = render_to_string('01epa_drupal_header.html', {})
    html = render_to_string('01epa_drupal_header.html', {
        'SITE_SKIN': os.environ['SITE_SKIN'],
        'TITLE': "CTS"
    })
    html += render_to_string('02epa_drupal_header_bluestripe_onesidebar.html', {})
    html += render_to_string('03epa_drupal_section_title_cts.html', {})
    html += render_to_string('06cts_ubertext_start_index_drupal.html', {
        'TITLE': header + ' Overview',
        'TEXT_PARAGRAPH': xx
    })
    html += render_to_string('07ubertext_end_drupal.html', {})
    html += links_left.ordered_list()  # fills out 05ubertext_links_left_drupal.html

    #scripts and footer
    html += render_to_string('09epa_drupal_ubertool_css.html', {})
    #html += render_to_string('09epa_drupal_ubertool_scripts.html', {})
    html += render_to_string('10epa_drupal_footer.html', {})


    response = HttpResponse()
    response.write(html)
    return response