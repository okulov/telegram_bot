import datetime

print(datetime.datetime.now().date())
print(''.join(['payments_',str(datetime.datetime.now().date()),'.xls']))