from django.template.loader import render_to_string
from collections import OrderedDict


# 03ubertext_links_left:
def linksLeft():
    link_dict = OrderedDict([
        ('Terrestrial Models', OrderedDict([
                ('Structural Analysis', 'analysis'),
                ('Chemical Editor', 'pchemprop'),
            ])
        ),
    ])

    html = render_to_string('03cts_ubertext_links_left.html', {'link_dict': link_dict})
    return html