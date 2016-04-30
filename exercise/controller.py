#coding:utf-8
from subject import settings
import os
import xlrd
from exercise.dao import exerciseDao
def fileCon(req):
    f_path = settings.MEDIA_ROOT + req['filename']
    with open(f_path,'wb+') as info:
        for chunk in req['file'].chunks():
            info.write(chunk)
    data=''
    tips = ''
    try:
        data = xlrd.open_workbook(f_path)
    except Exception,e:
        tips = str(e)
    table = data.sheets()[0]
    nrows = table.nrows #行数
    rs = []
    for i in range(1,nrows):
        cell_A1 = table.cell(i,0).value
        cell_A2 = table.cell(i,1).value
        cell_A3 = table.cell(i,2).value
        if cell_A1 and cell_A2 and cell_A3:    
            rs.append({'title':cell_A1,
                       'answer':cell_A2,
                       'tips':cell_A3})
        else:
            tips = "execl格式不正确"
    dao = exerciseDao({'userid':req['userid']})
    dao.insert_titles(rs)
    os.remove(f_path)
    tips = "添加成功"
    return tips 