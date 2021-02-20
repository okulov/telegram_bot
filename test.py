import datetime
import os

#print(datetime.datetime.now().date())
#print(''.join(['payments_',str(datetime.datetime.now().date()),'.xls']))

if not os.path.exists('download'):
    os.mkdir('download')
if not os.path.exists('download/input'):
    os.mkdir('download/input')
if not os.path.exists('download/output'):
    os.mkdir('download/output')