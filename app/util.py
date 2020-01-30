from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import datetime, timedelta


def sendmail(subject, template, to, context):
    template_str = 'app/' + template + '.html'
    html_msg = render_to_string(template_str, {'data': context})
    plain_msg = strip_tags(html_msg)
    from_email = 'ridham.shah.aditi@gmail.com'
    send_mail(subject, plain_msg, from_email, to, html_message=html_msg)