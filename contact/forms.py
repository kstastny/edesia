#coding=utf-8
#base taken from http://www.djangosnippets.org/snippets/261/

from django import forms as forms
from django.forms.widgets import Textarea
from django.core.mail import send_mail, BadHeaderError

# A simple contact form with four fields.
class ContactForm(forms.Form):
    name = forms.CharField(label='Jméno')
    email = forms.EmailField(label='Email')
    message = forms.CharField(widget=Textarea(), label='Zpráva')

