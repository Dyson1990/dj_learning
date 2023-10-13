# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 11:54:08 2022

@author: Weave
"""
import time
import json

from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

try:
    import minio
except:
    pass

class ChromeManager:
    
    def __init__(self):
        pass
    
    def __match_ver(self):
        pass
    
    def __from_minio(self, inner_dir):
        minio_cli = minio.Minio('192.168.1.23:19000',
                                access_key='minioadmin',
                                secret_key='minioadmin',
                                secure=False,
                                )
        








if __name__ == "__main__":
    pass