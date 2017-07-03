from django.template.loader import render_to_string
from collections import OrderedDict


# 03ubertext_links_left:
def ordered_list(model=None, page=None):
    link_dict = OrderedDict([
        ('CTS Workflows', OrderedDict([
                ('Calculate Chemical Speciation', 'cts/chemspec'),
                ('Calculate P-Chem Properties', 'cts/pchemprop'),
                ('Generate Transformation Products', 'cts/gentrans'),
            ])
        ),
        # ('About', OrderedDict([
        #         ('Chemical Editor', 'cts/module/chemedit-description'),
        #         ('P-Chem Properties', 'cts/module/pchemprop-description'),
        #         ('Reaction Pathway Simulator', 'cts/module/reactsim-description'),
        #     ])
        # ),
        ('About', OrderedDict([
                ('CTS Workflow Modules', 'cts/about/modules'),
                ('P-Chem Calculators', 'cts/about/pchemcalcs'),
                ('Reaction Libraries', 'cts/about/reactionlibs'),
            ])
        ),
        ('Documentation', OrderedDict([
                ('Download CTS User Guide', 'static_qed/cts/docs/CTS_USER_Guide_5-8-17.docx'),
                ('API Documentation', 'cts/rest/'),
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