#coding=utf-8

from django import forms
from django.contrib.comments.forms import CommentForm as DjangoCommentForm
from django.core.exceptions import ValidationError

def validate_captcha(value):
    if value.strip().upper() <> 'HAVEL':
        raise ValidationError('Nesprávný výsledek.')


class CommentForm(DjangoCommentForm):
    email         = forms.EmailField(label="Email", required=False)
    captcha       = forms.CharField(label=u"Pro vložení komentáře napište příjmení prvního prezidenta ČR (Václav H.)", 
            required=True,
            validators=[validate_captcha])
            #error_messages={'invalid': u'Nesprávný výsledek.'})
