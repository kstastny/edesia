from django import forms
from django.contrib.comments.forms import CommentForm as DjangoCommentForm

class CommentForm(DjangoCommentForm):
    email         = forms.EmailField(label="Email", required=False)

