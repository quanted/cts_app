from django.template.loader import render_to_string
from django.http import HttpResponse
import importlib
#import linksLeft
from .links_left import ordered_list
import os
from cts_app.models import cts_acronyms
from cts_app.models import cts_errors



def descriptionPage(request, model='none', header='none'):

    viewmodule = importlib.import_module('.views', 'cts_app.models.'+model)
    header = viewmodule.header
    text_file2 = open(os.path.join(os.environ['PROJECT_PATH'], 'cts_app/models/'+model+'/'+model+'_text.txt'),'r')
    xx = text_file2.read()

    #drupal template for header with bluestripe
    #html = render_to_string('01epa_drupal_header.html', {})
    html = render_to_string('01epa_drupal_header.html', {
        'SITE_SKIN': os.environ['SITE_SKIN'],
        'title': "CTS"
    })
    html += render_to_string('02epa_drupal_header_bluestripe_onesidebar.html', {})
    html += render_to_string('03epa_drupal_section_title_cts.html', {})

    html += render_to_string('06cts_ubertext_start_index_drupal.html', {
        'TITLE': header + ' Overview',
        'TEXT_PARAGRAPH': xx
    })
    html += render_to_string('07ubertext_end_drupal.html', {})
    html += ordered_list('cts/'+model)  # fills out 05ubertext_links_left_drupal.html

    #scripts and footer
    html += render_to_string('09epa_drupal_ubertool_css.html', {})
    html += render_to_string('09epa_drupal_cts_css.html')
    html += render_to_string('09epa_drupal_cts_scripts.html')
    #html += render_to_string('09epa_drupal_ubertool_scripts.html', {})
    html += render_to_string('10epa_drupal_footer.html', {})

    response = HttpResponse()
    response.write(html)
    return response


def about_page(request, model='none', header='non'):
    
    text_file2 = None

    if model == 'modules':
        text_file2 = open(os.path.join(os.environ['PROJECT_PATH'], 'static_qed/cts/docs/cts_modules_descriptions.txt'),'r')
        header = "CTS Modules"

    elif model == 'pchemcalcs':
        text_file2 = open(os.path.join(os.environ['PROJECT_PATH'], 'static_qed/cts/docs/cts_pchemcalcs_descriptions.txt'),'r')
        header = "Physicochemical Calculators"

    elif model == 'reactionlibs':
        text_file2 = open(os.path.join(os.environ['PROJECT_PATH'], 'static_qed/cts/docs/cts_reactionlibs_descriptions.txt'),'r')
        header = "Reaction Libraries"

    elif model == 'manuscripts':
        text_file2 = open(os.path.join(os.environ['PROJECT_PATH'], 'static_qed/cts/docs/cts_manuscripts_descriptions.txt'),'r')
        header = "CTS Manuscripts"

    elif model == 'acronyms':
        # renders django template to display acronyms table:
        acronyms_table = render_to_string('cts_acronyms_table.html', {'cts_acronyms_list': cts_acronyms.acronyms})
        header = "CTS Acronyms"

    elif model == 'flowcharts':
        text_file2 = open(os.path.join(os.environ['PROJECT_PATH'], 'static_qed/cts/docs/cts_flowcharts_descriptions.txt'),'r')
        header = "CTS Flowcharts"

    elif model == 'intendeduse':
        text_file2 = open(os.path.join(os.environ['PROJECT_PATH'], 'static_qed/cts/docs/cts_intended_use.txt'),'r')
        header = "Intended Use"

    elif model == 'errors':
        errors_table = render_to_string('cts_errors_table.html', {'cts_errors_list': cts_errors.cts_errors})
        header = "CTS Errors"

    #drupal template for header with bluestripe
    html = render_to_string('01epa_drupal_header.html', {
        'SITE_SKIN': os.environ['SITE_SKIN'],
        'title': "CTS"
    })
    html += render_to_string('02epa_drupal_header_bluestripe_onesidebar.html', {})
    html += render_to_string('03epa_drupal_section_title_cts.html', {})

    if text_file2:
        xx = text_file2.read()
        html += render_to_string('06cts_ubertext_start_index_drupal.html', {
            'TITLE': header,
            'TEXT_PARAGRAPH': xx
        })
    elif model == 'acronyms':
        html += render_to_string('06cts_ubertext_start_index_drupal.html', {
            'TITLE': header,
            'TEXT_PARAGRAPH': acronyms_table
        })
    elif model == 'errors':
        html += render_to_string('06cts_ubertext_start_index_drupal.html', {
            'TITLE': header,
            'TEXT_PARAGRAPH': errors_table
        })

    html += render_to_string('07ubertext_end_drupal.html', {})
    html += ordered_list()  # fills out 05ubertext_links_left_drupal.html

    #scripts and footer
    html += render_to_string('09epa_drupal_ubertool_css.html', {})
    html += render_to_string('10epa_drupal_footer.html', {})

    response = HttpResponse()
    response.write(html)
    return response



def flowcharts_page(request, chart='none', header='non'):
    
    img_filepath = None

    if chart == 'cheminfo':
        # displays chemical information flowchart
        img_filepath = '/static_qed/cts/docs/cts_flowchart_cheminfo.svg'
        header = ""

    elif chart == 'standardization':
        # displays standardization flowchart
        img_filepath = '/static_qed/cts/docs/cts_flowchart_smilesfilter.svg'
        header = ""

    elif chart == 'meltingpoint':
        # displays melting point request flowchart
        img_filepath = '/static_qed/cts/docs/cts_flowchart_meltingpoint.svg'
        header = ""

    #drupal template for header with bluestripe
    html = render_to_string('01epa_drupal_header.html', {
        'SITE_SKIN': os.environ['SITE_SKIN'],
        'title': "CTS"
    })
    html += render_to_string('02epa_drupal_header_bluestripe_onesidebar.html', {})
    html += render_to_string('03epa_drupal_section_title_cts.html', {})

    if img_filepath:
        html += """
        <div class="main-column clearfix">
        <div class="panel-pane pane-node-content" >
          <div class="pane-content">
            <div class="node node-page clearfix view-mode-full">
                <object type="image/svg+xml" data="{}"></object>
        """.format(img_filepath)

    html += render_to_string('07ubertext_end_drupal.html', {})
    html += ordered_list()  # fills out 05ubertext_links_left_drupal.html

    #scripts and footer
    html += render_to_string('09epa_drupal_ubertool_css.html', {})
    html += render_to_string('10epa_drupal_footer.html', {})

    response = HttpResponse()
    response.write(html)
    return response