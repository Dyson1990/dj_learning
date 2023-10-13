# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 10:08:42 2022

@author: Weave
"""
import sys
from pathlib import Path
py_dir = Path(__file__).parent
app_dir = py_dir.parent
sys.path.append(app_dir.as_posix())
sys.path.append(py_dir.as_posix())

import re

import spider
import file_manager
import redis_conn
import minio_conn

def linkedin_com_m10(ori_url, cookie_str, testing=False):
    # 10月国庆特别版
    
    if testing:
        return 'mark：部署好后未测试，暂停使用'
    log_id = re.search(r'(?<=/)\d+(?=/)', ori_url).group()
    spider.get_data_from_network(ori_url, cookie_str, log_id)
    
    pn = 1
    fn = f'{log_id}.xlsx'
    fp = py_dir.join('tmp', fn)
    while True:
        object_name = f'linkedin_com/json/{log_id}_pn{pn}.json'
        json_str = minio_conn.get_file(object_name)
        
        if json_str is None:
            break
        
        for row in spider.parse_json(json_str):
            file_manager.update_xlsx(row, fp)
    
    inner_path = 'linkedin_com/xlsx'
    minio_conn.put_one_file(fp, inner_path)
    
    return minio_conn.get_url(f'{inner_path}/{fn}')