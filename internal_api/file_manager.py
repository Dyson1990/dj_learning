# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 14:13:33 2022

@author: Weave
"""
import sys
from pathlib import Path
py_dir = Path(__file__).parent
app_dir = py_dir.parent
sys.path.append(app_dir.as_posix())

import openpyxl

def update_xlsx(row:dict, fp:Path):
    if not fp.exists():
        wb = openpyxl.Workbook()
        wb.save(fp)
        wb.close()
        
    if not row:
        return None
        
    wb = openpyxl.load_workbook(fp)
    ws = wb.active
    
    if len(list(ws.rows)) == 0:
        title = list(row.keys())
        ws.append(title)
    else:
        title = [c0.value for c0 in next(ws.rows)]
        
    data = [tup0[1] for tup0 in sorted(row.items(), key=lambda tup0: title.index(tup0[0]))]
    ws.append(data)
    
    wb.save(fp)
    wb.close()
        
if __name__ == "__main__":
    update_xlsx({"A": 12, "B": 345}, py_dir.joinpath('test.xlsx'))