from django.template.loader import render_to_string
from collections import OrderedDict


# 03ubertext_links_left:
def linksLeft():
    link_dict = OrderedDict([
        ('CTS Workflows', OrderedDict([
                ('Calculate Chemical Speciation', 'chemspec'),
                ('Calculate Physicochemical Properties', 'pchemprop'),
                ('Generate Transformation Products', 'gentrans'),
            ])
        ),
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

    html = render_to_string('03cts_ubertext_links_left.html', {'link_dict': link_dict})
    return html