import string, random, re
from django.conf import settings
from django.utils.translation import gettext as _
import json
from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMultiAlternatives

def random_generate( size = 26, chars = string.ascii_uppercase + string.digits ):
    return ''.join( random.choice( chars ) for x in range( size ) )

def send_email(subject, template, to, variables={}, attachment=None):

    if not type(to) == list:
        to = [to]
    template = get_template(template)
    context = Context(variables)
    htmlContent = template.render(context).encode('utf8')

    text_content = 'This is an important message.'
    msg = EmailMultiAlternatives(
        subject,
        text_content,
        "Project <%s>" % (settings.DEFAULT_FROM_EMAIL),
        to)
    msg.attach_alternative(htmlContent, "text/html")

    if attachment:
        msg.attach(
            attachment['file_name'],
            attachment['file_location'],
            attachment['file_type'])

    msg.send()
