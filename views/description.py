from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import BadHeaderError, send_mail
import importlib
from .links_left import ordered_list
import os
import logging
from cts_app.models import cts_acronyms, cts_errors, cts_measured_refs
from django.conf import settings



def descriptionPage(request, model='none', header='none'):

    viewmodule = importlib.import_module('.views', 'cts_app.models.'+model)
    header = viewmodule.header
    text_file2 = open(os.path.join(os.environ['PROJECT_PATH'], 'models', model, model+'_text.txt'),'r')
    xx = text_file2.read()

    #drupal template for header with bluestripe
    #html = render_to_string('cts_app/01cts_epa_drupal_header.html', {})
    html = render_to_string('cts_app/01cts_epa_drupal_header.html', {
        'SITE_SKIN': os.environ['SITE_SKIN'],
        'title': "CTS"
    })
    html += render_to_string('cts_app/02epa_drupal_header_bluestripe_onesidebar.html', {})
    html += render_to_string('cts_app/03epa_drupal_section_title_cts.html', {"version": os.getenv("CTS_VERSION")})

    html += render_to_string('cts_app/06cts_ubertext_start_index_drupal.html', {
        'TITLE': header + ' Overview',
        'TEXT_PARAGRAPH': xx
    })
    html += render_to_string('cts_app/07ubertext_end_drupal.html', {})
    html += ordered_list('cts/'+model)  # fills out 05ubertext_links_left_drupal.html

    #scripts and footer
    html += render_to_string('cts_app/09epa_drupal_ubertool_css.html', {})
    html += render_to_string('cts_app/09epa_drupal_cts_css.html')
    html += render_to_string('cts_app/09epa_drupal_cts_scripts.html')
    #html += render_to_string('cts_app/09epa_drupal_ubertool_scripts.html', {})
    html += render_to_string('cts_app/10epa_drupal_footer.html', {})

    response = HttpResponse()
    response.write(html)
    return response


def about_page(request, model='none', header='non'):
    
    text_file2, html_string = None, None

    if model == 'cts':
        html_string = render_to_string('cts_app/cts_about.html')
        header = "About CTS"

    elif model == 'modules':
        # text_file2 = open(os.path.join(os.environ['PROJECT_PATH'], 'collected_static/cts_app/docs/cts_modules_descriptions.txt'),'r')
        text_file2 = open(os.path.join(settings.STATIC_ROOT, 'cts_app', 'docs', 'cts_modules_descriptions.txt'),'r')
        header = "CTS Modules"

    elif model == 'pchemcalcs':
        # text_file2 = open(os.path.join(os.environ['PROJECT_PATH'], 'collected_static/cts_app/docs/cts_pchemcalcs_descriptions.txt'),'r')
        text_file2 = open(os.path.join(settings.STATIC_ROOT, 'cts_app', 'docs', 'cts_pchemcalcs_descriptions.txt'),'r')
        header = "Physicochemical Property Calculators"

    elif model == 'reactionlibs':
        # text_file2 = open(os.path.join(os.environ['PROJECT_PATH'], 'collected_static/cts_app/docs/cts_reactionlibs_descriptions.txt'),'r')
        text_file2 = open(os.path.join(settings.STATIC_ROOT, 'cts_app', 'docs', 'cts_reactionlibs_descriptions.txt'),'r')
        header = "Reaction Libraries"

    elif model == 'manuscripts':
        # text_file2 = open(os.path.join(os.environ['PROJECT_PATH'], 'collected_static/cts_app/docs/cts_manuscripts_descriptions.txt'),'r')
        text_file2 = open(os.path.join(settings.STATIC_ROOT, 'cts_app', 'docs', 'cts_manuscripts_descriptions.txt'),'r')
        header = "CTS Manuscripts"

    elif model == 'acronyms':
        # renders django template to display acronyms table:
        html_string = render_to_string('cts_app/cts_acronyms_table.html', {'cts_acronyms_list': cts_acronyms.acronyms})
        header = "CTS Acronyms"

    elif model == 'flowcharts':
        # text_file2 = open(os.path.join(os.environ['PROJECT_PATH'], 'collected_static/cts_app/docs/cts_flowcharts_descriptions.txt'),'r')
        text_file2 = open(os.path.join(settings.STATIC_ROOT, 'cts_app', 'docs', 'cts_flowcharts_descriptions.txt'),'r')
        header = "CTS Flowcharts"

    elif model == 'help':
        # text_file2 = open(os.path.join(os.environ['PROJECT_PATH'], 'collected_static/cts_app/docs/cts_help.txt'),'r')
        text_file2 = open(os.path.join(settings.STATIC_ROOT, 'cts_app', 'docs', 'cts_help.txt'),'r')
        header = "Help"

    elif model == 'errors':
        html_string = render_to_string('cts_app/cts_errors_table.html', {'cts_errors_list': cts_errors.cts_errors})
        header = "CTS Errors"

    elif model == 'contact':
        # text_file2 = open(os.path.join(os.environ['PROJECT_PATH'], 'collected_static/cts_app/docs/cts_contact.txt'),'r')
        # text_file2 = open(os.path.join(settings.STATIC_ROOT, 'cts_app', 'docs', 'cts_contact.txt'),'r')
        html_string = render_to_string('cts_app/cts_contacts_page.html', {}, request=request)
        header = "CTS Contact"

    elif model == 'versionhistory':
        # text_file2 = open(os.path.join(os.environ['PROJECT_PATH'], 'collected_static/cts_app/docs/cts_version_history.txt'),'r')
        text_file2 = open(os.path.join(settings.STATIC_ROOT, 'cts_app', 'docs', 'cts_version_history.txt'),'r')
        header = "CTS Version History"

    elif model == 'measured-pka-refs':
        # renders django template to display measured pka refs table:
        html_string = render_to_string('cts_app/cts_measured_refs.html',
            {
                'cts_measured_refs': cts_measured_refs.cts_measured_refs,
                'cts_measured_refs_headers': cts_measured_refs.cts_measured_refs_headers
            })
        header = "CTS Acronyms"

    #drupal template for header with bluestripe
    html = render_to_string('cts_app/01cts_epa_drupal_header.html', {
        'SITE_SKIN': os.environ['SITE_SKIN'],
        'title': "CTS"
    })
    html += render_to_string('cts_app/02epa_drupal_header_bluestripe_onesidebar.html', {})
    html += render_to_string('cts_app/03epa_drupal_section_title_cts.html', {"version": os.getenv("CTS_VERSION")})

    if text_file2:
        xx = text_file2.read()
        html += render_to_string('cts_app/06cts_ubertext_start_index_drupal.html', {
            'TITLE': header,
            'TEXT_PARAGRAPH': xx
        })
    elif html_string:
        html += render_to_string('cts_app/06cts_ubertext_start_index_drupal.html', {
            'TITLE': header,
            'TEXT_PARAGRAPH': html_string
        })

    html += render_to_string('cts_app/07ubertext_end_drupal.html', {})
    html += ordered_list()  # fills out 05ubertext_links_left_drupal.html

    #scripts and footer
    html += render_to_string('cts_app/09epa_drupal_ubertool_css.html', {})
    html += render_to_string('cts_app/10epa_drupal_footer.html', {})

    response = HttpResponse()
    response.write(html)
    return response



def flowcharts_page(request, chart='none', header='non'):
    
    img_filepath = None

    if chart == 'cheminfo':
        # displays chemical information flowchart
        img_filepath = settings.STATIC_URL + 'cts_app/docs/cts_flowchart_cheminfo.svg'
        header = ""

    elif chart == 'standardization':
        # displays standardization flowchart
        img_filepath = settings.STATIC_URL + 'cts_app/docs/cts_flowchart_smilesfilter.svg'
        header = ""

    elif chart == 'meltingpoint':
        # displays melting point request flowchart
        img_filepath = settings.STATIC_URL + 'cts_app/docs/cts_flowchart_meltingpoint.svg'
        header = ""

    #drupal template for header with bluestripe
    html = render_to_string('cts_app/01cts_epa_drupal_header.html', {
        'SITE_SKIN': os.environ['SITE_SKIN'],
        'title': "CTS"
    })
    html += render_to_string('cts_app/02epa_drupal_header_bluestripe_onesidebar.html', {})
    html += render_to_string('cts_app/03epa_drupal_section_title_cts.html', {"version": os.getenv("CTS_VERSION")})

    if img_filepath:
        html += """
        <div class="main-column clearfix">
        <div class="panel-pane pane-node-content" >
          <div class="pane-content">
            <div class="node node-page clearfix view-mode-full">
                <object type="image/svg+xml" data="{}"></object>
        """.format(img_filepath)

    html += render_to_string('cts_app/07ubertext_end_drupal.html', {})
    html += ordered_list()  # fills out 05ubertext_links_left_drupal.html

    #scripts and footer
    html += render_to_string('cts_app/09epa_drupal_ubertool_css.html', {})
    html += render_to_string('cts_app/10epa_drupal_footer.html', {})

    response = HttpResponse()
    response.write(html)
    return response