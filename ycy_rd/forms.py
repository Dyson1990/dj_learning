# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 16:23:28 2022

@author: Weave
"""
import datetime

from django import forms
from django.core import validators

class FileFieldForm(forms.Form):
    email = forms.CharField(max_length=30, validators=[validators.RegexValidator(regex=r'.+@trade-ai.com', message='Invalid Imgur email')])
    cookies = forms.CharField(required=False)
    # create_time = forms.DateTimeField(initial=datetime.datetime.now())
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))