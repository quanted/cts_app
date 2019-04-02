from django.template.loader import render_to_string
from collections import OrderedDict

# 03ubertext_links_left:
def ordered_list(model=None, page=None):
    link_dict = OrderedDict([
        ('About', OrderedDict([
                # ('CTS Modules', 'cts/about/modules'),
                ('About CTS', 'cts/about/cts'),
                ('Contact', 'cts/about/contact'),
            ])
        ),
        ('Execute CTS Workflows', OrderedDict([
                ('Calculate Chemical Speciation', 'cts/chemspec'),
                ('Calculate Physicochemical Properties', 'cts/pchemprop'),
                ('Generate Transformation Products', 'cts/gentrans'),
            ])
        ),
        ('Documentation', OrderedDict([
                ("Download CTS User's Guide (PDF)", 'static_qed/cts/docs/CTS_USER_Guide_10-03-2018.pdf'),
                ('CTS Modules', 'cts/about/modules'),
                ('Physicochemical Calculators', 'cts/about/pchemcalcs'),
                ('Reaction Libraries', 'cts/about/reactionlibs'),
                ('API Documentation', 'cts/rest/'),
                ('Manuscripts', 'cts/about/manuscripts'),
                ('Intended Use', 'cts/about/intendeduse'),
                ('Version History', 'cts/about/versionhistory'),
                # ('CTS Acronyms', 'cts/about/acronyms'),
                # ('CTS Flowcharts', 'cts/about/flowcharts'),
                # ('CTS Errors', 'cts/about/errors'),
                # ('Source Code', 'https://github.com/quanted/cts_app'),
            ])
        )
    ])

    return render_to_string('03ubertext_links_left_drupal_cts.html', {
        'LINK_DICT': link_dict,
        'MODEL': model,
        'PAGE': page
    })