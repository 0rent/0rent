# import re

import logging
from django.template import Library
# from django.utils.encoding import smart_text
# from django.utils.translation import ugettext_lazy as _
# from django.core.urlresolvers import reverse

LOGGER = logging.getLogger(__name__)

register = Library()


@register.filter
def percent(number, total):
    """ return a percentage of number from total """

    # tag: {% percent owner.counter product.nb_use %}
    # filter: {{ owner.counter|percent:product.nb_use }}

    return '{0:.2f}'.format(number * 100.0 / total)
