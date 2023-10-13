# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 14:52:25 2022

@author: Weave
"""
import sys
from pathlib import Path
py_dir = Path(__file__).parent
app_dir = py_dir.parent
sys.path.append(app_dir.as_posix())

import time
import json

from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

import app_logger as lg

driver_dir = app_dir.parent.joinpath('tools')
proxies = {'http':'socks5://127.0.0.1:10808', 'https':'socks5://127.0.0.1:10808'}

def driver_with_log():
    global proxies, driver_dir
    
    chrome_options = Options()
    chrome_options.add_argument('--log-level=1')  # 忽略错误
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    chrome_options.add_argument('--ignore-certificate-errors')  # 忽略证书错误
    chrome_options.add_argument('--headless')  # 开启无头模式
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-application-cache') # 禁用缓存
    
    chrome_options.add_argument('--proxy-server=' + proxies['http'])
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--start-maximized")
    # chrome_options.add_argument("--window-size=1920x1080")  # I added this
    
    chrome_options.add_argument('x-li-lang=en_US')
    chrome_options.add_argument('x-restli-protocol-version=2.0.0')

    caps = {
        'browserName': 'chrome',
        'goog:loggingPrefs': {
            'browser': 'ALL',
            'driver': 'ALL',
            'performance': 'ALL',
        },
        'goog:chromeOptions': {
            'perfLoggingPrefs': {
                'enableNetwork': True,
            },
            'w3c': False,
        },
    }
    server = Service(str(driver_dir.joinpath('chromedriver106_win.exe')))
    driver = webdriver.Chrome(service=server
                              , desired_capabilities=caps
                              , options=chrome_options
                              )
    return driver

def get_network(url, cookie_str, fn, **args):
    while True:
        try:
            lg.driver_info('准备访问:', url)
            driver = driver_with_log()
            driver.get(url)
            
            cookie_dict = dict([s0.split('=', maxsplit=1) for s0 in cookie_str.split('; ')])
            for k0, v0 in cookie_dict.items():
                driver.add_cookie({"name": k0, "value": v0, 'domain': 'www.linkedin.com'})
            # driver.get(url)
            driver.refresh()
            
            time.sleep(8)
            
            logs = [json.loads(log['message'])['message'] for log in driver.get_log('performance')]
            html = driver.page_source
            
            driver.close()
            return html, logs

        except Exception as err:
            lg.driver_info('垃圾网站，不返数据，准备重试!!!')
            driver.close()
            
            lg.print_exc(err)
            time.sleep(5)