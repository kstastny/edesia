import re
import string


from django import template
from django.template.defaultfilters import stringfilter, escape
from django.utils.functional import allow_lazy
from django.utils.safestring import mark_safe, SafeData
from django.utils.encoding import force_unicode

register = template.Library()

@register.filter
def linebreaksp(value, autoescape=None):
    """ Converts newlines into <p>s."""
    value = re.sub(r'\r\n|\r|\n', '\n', force_unicode(value)) # normalize newlines
    value = re.sub(r'\n{2,}','\n', value) #remove additional newlines = replace \n\n\n with \n
    paras = re.split('\n', value)
    if autoescape:
        paras = [u'<p>%s</p>' % escape(p) for p in paras]
    else:
        paras = [u'<p>%s</p>' % p for p in paras]
    return mark_safe(u'\n'.join(paras))
linebreaksp = allow_lazy(linebreaksp, unicode)
linebreaksp.is_safe = True
linebreaksp.needs_autoescape = True
linebreaksp = stringfilter(linebreaksp)

if __name__ == "__main__":
    print linebreaksp('toto\nje nejaky\n\nretezec\n\n\n\ns konci radku')
