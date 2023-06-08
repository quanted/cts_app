from django.template.loader import render_to_string
from collections import OrderedDict
import os

# 03ubertext_links_left:
def ordered_list(model=None, page=None):
    link_dict = OrderedDict([
        ('About', OrderedDict([
                ('CTS Home', 'cts/'),
                ('CTS Basic Information', 'cts/about/cts'),
                # ('Contact', 'cts/about/contact'),
            ])
        ),
        ('Execute CTS Workflows', OrderedDict([
                ('Calculate Chemical Speciation', 'cts/chemspec'),
                ('Calculate Physicochemical Properties', 'cts/pchemprop'),
                ('Generate Transformation Products', 'cts/gentrans'),
            ])
        ),
        ('Documentation', OrderedDict([
                ("CTS User's Guide", 'cts/static/cts_app/docs/CTSv2_User_Guide_20230403.pdf'),
                # ("CTS User's Guide", 'https://www.epa.gov/chemical-research/users-guide-chemical-transformation-simulator-cts'),
                ('CTS Modules', 'cts/about/modules'),
                ('Property Calculators', 'cts/about/pchemcalcs'),
                ('Reaction Libraries', 'cts/about/reactionlibs'),
                ('API Documentation', 'cts/rest/'),
                ('Manuscripts', 'cts/about/manuscripts'),
                ('Version History', 'cts/about/versionhistory'),
                ('Help', 'cts/about/help'),
            ])
        )
    ])

    return render_to_string('cts_app/03ubertext_links_left_drupal_cts.html', {
        'LINK_DICT': link_dict,
        'MODEL': model,
        'PAGE': page
    })