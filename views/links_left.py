from django.template.loader import render_to_string
from collections import OrderedDict


# 03ubertext_links_left:
def ordered_list(model=None, page=None):
    link_dict = OrderedDict([
        ('Execute CTS Workflows', OrderedDict([
                ('Calculate Chemical Speciation', 'cts/chemspec'),
                ('Calculate Physicochemical Properties', 'cts/pchemprop'),
                ('Generate Transformation Products', 'cts/gentrans'),
            ])
        ),
        # ('About', OrderedDict([
        #         ('Chemical Editor', 'cts/module/chemedit-description'),
        #         ('Physicochemical Properties', 'cts/module/pchemprop-description'),
        #         ('Reaction Pathway Simulator', 'cts/module/reactsim-description'),
        #     ])
        # ),
        ('About', OrderedDict([
                ('CTS Modules', 'cts/about/modules'),
                ('Physicochemical Calculators', 'cts/about/pchemcalcs'),
                ('Reaction Libraries', 'cts/about/reactionlibs'),
            ])
        ),
        ('Documentation', OrderedDict([
                # ('Download CTS User Guide (PDF)', 'static_qed/cts/docs/CTS_USER_Guide_5-8-17.pdf'),
                ('Download CTS User Guide (PDF)', 'static_qed/cts/docs/CTS_USER_Guide_7-19-2018.pdf'),
                ('API Documentation', 'cts/rest/'),
                ('Manuscripts', 'cts/about/manuscripts'),
                ('CTS Acronyms', 'cts/about/acronyms')
                # ('Source Code', 'https://github.com/quanted/cts_app'),
            ])
        ),
        # ('')
        # ('Access Databases', OrderedDict([
        # 		('FIFRA Chemicals', 'fifra'),
        # 		('Flame Retardants', 'flame'),
        # 	])
        # ),
        # ('Reaction Library Databases', OrderedDict([
        # 		('Abiotic Hydrolysis', 'ahydrolysis'),
        # 		('Abiotic Reduction', 'areduction'),
        # 		('Mammalian Metabolism', 'mammet'),
        # 	])
        # ),
    ])

    # html = render_to_string('03cts_ubertext_links_left.html', {'link_dict': link_dict})
    # return html

    return render_to_string('03ubertext_links_left_drupal_cts.html', {
        'LINK_DICT': link_dict,
        'MODEL': model,
        'PAGE': page
    })