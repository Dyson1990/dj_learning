# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 16:36:23 2022

@author: Weave
"""
from django.db import models

# 自定义验证器
from django.core import validators


class UploadFileModel(models.Model):
    # 当我们想设置最小长度的时候，但是在字段中没有的话，可以借助自定义验证器
    # MinLengthValidator
    email = models.CharField(max_length=30, validators=[validators.RegexValidator(regex=r'.+@trade-ai.com', message='Invalid Imgur email')])
    cookies = models.TextField()
    author = models.FileField()
    create_time = models.DateTimeField(auto_now_add=True)
