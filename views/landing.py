from django.template.loader import render_to_string
from django.http import HttpResponse
import importlib
from .links_left import ordered_list
import os
import logging
import bleach


def ctsLandingPage(request):

    html = render_to_string('01epa_drupal_header.html', {
        'SITE_SKIN': os.environ['SITE_SKIN'],
        'title': "CTS"
    })

    html += render_to_string('02epa_drupal_header_bluestripe_onesidebar.html', {})

    if os.getenv("ENV_NAME") == 'cgi_azure_docker_dev':
        html += render_to_string('03epa_drupal_section_title_cts.html',
            {
                "message": bleach.clean('<b>NOTICE:</b> CTS is moving to \
                    <a href="https://qed.epa.gov/cts">qed.epa.gov/cts</a> in the near future.<br>')
            }
        )
    else:
        html += render_to_string('03epa_drupal_section_title_cts.html', {"message": ""})

    main_text_html = render_to_string('cts_landing_text.html', {})
    html += render_to_string('06cts_ubertext_start_index_drupal.html', {
        'TEXT_PARAGRAPH': main_text_html
    })

    html += render_to_string('07ubertext_end_drupal.html', {})
    html += ordered_list(model='cts')  # fills out 05ubertext_links_left_drupal.html

    #scripts and footer
    html += render_to_string('09epa_drupal_ubertool_css.html', {})
    html += render_to_string('09epa_drupal_cts_css.html')
    html += render_to_string('09epa_drupal_cts_scripts.html')
    html += render_to_string('10epa_drupal_footer.html', {})

    response = HttpResponse()
    response.write(html)

    return response