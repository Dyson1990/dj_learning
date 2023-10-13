# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 11:05:34 2022

@author: Weave
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 16:06:10 2022

@author: Weave
"""

import traceback

from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

from django.views.generic.edit import FormView
from .forms import FileFieldForm
from internal_api.ocr import ocr

def home(request):
    return render(request, 'home/index.html')


class FileFieldFormView(FormView):
    form_class = FileFieldForm
    template_name = 'post/common.html'  # Replace with your template.
    success_url = '/post'# 'post/'  # Replace with your URL or reverse().
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file')
        api_type = request.POST.get('api')

        if form.is_valid():
            if api_type == 'ocr':
                res_l = []
                for memory_file in files:
                    try:
                        text = ocr.from_bytes(memory_file.read())
                        res_l.append(text)
                    except:
                        traceback.print_exc()
                        res_l.append('# error: 无法读取图片文件')
                # print('res_l:', res_l)
                return HttpResponse('\n'.join(res_l))
            else:
                return self.form_valid(form)
        else:
            print('form err')
            return self.form_invalid(form)