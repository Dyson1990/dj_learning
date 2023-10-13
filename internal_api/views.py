# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 16:06:10 2022

@author: Weave
"""

from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt

import codecs
import base64

from .linkedin_com import ctrl
from .ocr import ocr

def surprise(request):
    # html_path = root_dir.joinpath('surprise', 'index.html')
    # with html_path.open('r') as fr:
    #     return fr.read()
    return render(request, 'surprise/index.html')

def linkedin_com_get(request):
    # 写进django后未测试
    return HttpResponse(ctrl.linkedin_com_m10('', '', testing=True))

@csrf_exempt
def api_ocr(request):
    if request.method == 'POST':
        if "img" in request.FILES:
            # print("from img")
            file0 = request.FILES.pop("img")[0]
            byte_str = file0.read()
        elif "bytes" in request.POST.keys():
            s0 = request.POST.get("bytes")
            byte_str = codecs.escape_decode(s0)[0]
            # 待研究np.fromstring(img_byte, np.uint8) 
        elif "base64" in request.POST.keys():
            # print("from base64")
            s0 = request.POST.get("base64")
            byte_str = base64.b64decode(s0.encode('utf-8'))
            # print(byte_str)
        return HttpResponse(ocr.from_bytes(byte_str))
    else:
        return HttpResponse('此api不接受get方法')