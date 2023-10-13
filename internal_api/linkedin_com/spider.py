# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 11:36:52 2022

@author: Weave
"""
import sys
from pathlib import Path
py_dir = Path(__file__).parent
app_dir = py_dir.parent
sys.path.append(app_dir.as_posix())

import json
import requests
import parsel

import driver_manager
import minio_conn


proxies = {'http':'socks5://127.0.0.1:10808', 'https':'socks5://127.0.0.1:10808'}

def get_data_from_network(url, cookie_str, log_id, ):
    pn = 1
    while True:
        html, logs = driver_manager.get_network(url, cookie_str)
        
        for d0 in logs:
            if d0['method'] == 'Network.requestWillBeSent' \
            and 'request' in d0['params'] \
            and d0['params']['request']['url'].endswith('talentRecruiterSearchHits'):
                data = d0['params']['request']['postData']
                headers = d0['params']['request']['headers']
                
                break
        
        headers['cookie'] = cookie_str
        headers['x-li-lang'] = 'en_US'
        b0 = if_last_page(html, pn)
        
        resp = requests.post('https://www.linkedin.com/talent/search/api/talentRecruiterSearchHits'
                             , headers=headers
                             , data=data
                             , proxies=proxies
                             )
        
        json_data = resp.json()
        minio_conn.put_string(json.dumps(json_data, indent=2, ensure_ascii=False)
                              , f'linkedin_com/json/{log_id}_pn{pn}.json'
                              )
        if b0:
            break
        else:
            pn = pn + 1
            url = url + '?start=' + str((pn-1)*25)

def if_last_page(html, pn):
    sel = parsel.Selector(html)
    
    if sel.xpath('//section[@data-test-empty-state-no-active-candidates="true"]'):
        return True
    
    e_div = sel.xpath('//div[@class="pagination__quick-link-wrapper"]')
    if not e_div:
        raise Exception('页面错误或未加载完整')

    if e_div.xpath('./a[@rel="next"]'):
        return False
    else:
        return True
    
def parse_json(json_str):
    json_data = json.loads(json_str)
    ele_list = json_data['elements']
    for ele0 in ele_list:
        row_data = ele0.get('linkedInMemberProfileUrnResolutionResult', {})
        if not row_data:
            continue
        
        we_func = lambda d0: d0.get('companyName', '')\
                             + '-'\
                             + d0.get('title', '')\
                             + '·' if 'startDateOn' in d0 else ''\
                             + '/'.join(filter(lambda s0: bool(s0), [d0.get('startDateOn', {}).get('year')
                                                                     , d0.get('startDateOn', {}).get('month')
                                                                     ]
                                               )
                                        )\
                             + '-' if 'startDateOn' in d0 else ''\
                             + '/'.join(filter(lambda s0: bool(s0), [d0.get('endDateOn', {}).get('year')
                                                                     , d0.get('endDateOn', {}).get('month')
                                                                     ]
                                               )
                                        )\
                             + 'Present' if 'endDateOn' not in d0 and 'startDateOn' in d0 else ''
        first_name = row_data.get('firstName', '').strip()
        last_name = row_data.get('lastName', '').strip()
        name_l = (first_name + ' ' + last_name).split(' ')
        
        output = {
            'FirstName': first_name
            , 'LastName': last_name
            , 'name1': name_l[0] if len(name_l) > 0 else ''
            , 'name2': name_l[1] if len(name_l) > 1 else ''
            , 'name3': ' '.join(name_l[2:]) if len(name_l) > 2 else ''
            , 'Domain': ''
            , 'Mail1': "=IF(OR(ISBLANK({c0}), ISBLANK({c1})),\"\",CONCATENATE(LOWER(TRIM({c0})),\".\", LOWER(TRIM({c1})), \"@\",{c2}))"
            , 'Mail2': "=IF(ISBLANK({c0}),\"\",CONCATENATE(LOWER(TRIM({c0})), \"@\",{c2}))"
            , 'Mail3': "=IF(ISBLANK({c1}),\"\",CONCATENATE(LOWER(TRIM({c1})), \"@\",{c2}))"
            , 'Mail4': "=IF(OR(ISBLANK({c0}), ISBLANK({c1})),\"\",CONCATENATE(LOWER(TRIM({c0})),LOWER(LEFT({c1},1)),\"@\",{c2}))"
            , 'Mail5': "=IF(OR(ISBLANK({c0}), ISBLANK({c1})),\"\",CONCATENATE(LOWER(LEFT({c0},1)),LOWER(TRIM({c1})), \"@\",{c2}))"
            , 'Mail6': "=IF(OR(ISBLANK({c0}), ISBLANK({c1})),\"\",CONCATENATE(LOWER(TRIM({c0})), LOWER(TRIM({c1})), \"@\",{c2}))"
            , 'Mail7': "=IF(OR(ISBLANK({c0}), ISBLANK({c1})),\"\",CONCATENATE(LOWER(TRIM({c0})),\"_\", LOWER(TRIM({c1})), \"@\",{c2}))"
            , 'Mail8': "=IF(OR(ISBLANK({c0}),ISBLANK({c1})),\"\",CONCATENATE(LOWER(TRIM({c0})),\".\",LOWER(LEFT({c1},1)),\"@\",{c2}))"
            , 'Mail9': "=IF(OR(ISBLANK({c0}),ISBLANK({c1})),\"\",CONCATENATE(LOWER(LEFT({c0},1)),\".\",LOWER(TRIM({c1})),\"@\",{c2}))"
            , 'Mail10': "=IF(OR(ISBLANK({c0}),ISBLANK({c1})),\"\",CONCATENATE(LOWER(LEFT({c0},1)),LOWER(LEFT({c1},1)),\"@\",{c2}))"
            , 'Name': first_name + ' ' + last_name
            , 'Headline': row_data.get('headline', '')
            , 'Location': row_data.get('location', {}).get('displayName', '')
            , 'IndustryName': row_data.get('industryName', '')
            , 'WorkExperience': '\n'.join([we_func(d0) for d0 in row_data.get('workExperience', [])])
        }
        yield output
    
